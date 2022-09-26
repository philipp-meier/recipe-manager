import json
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.shortcuts import render
from django.utils import translation
from django.urls import reverse
from django.conf import settings

from .forms import RecipeForm
from .models import User, Recipe, RecipeIngredient
from .helper import update_recipe_ingredients, to_recipe_data_transfer_objects


@login_required(login_url='/login')
def index(request):
    """Renders the start page with a specific amount of recipe suggestions."""
    amount_param = request.GET.get("amount")

    if not amount_param or not amount_param.isnumeric() or not int(amount_param) >= 1:
        amount = settings.DEFAULT_SUGGESTION_AMOUNT
    else:
        amount = int(amount_param)

    data_transfer_objects = to_recipe_data_transfer_objects(
        random.sample(list(Recipe.objects.all()), min(int(amount), Recipe.objects.count())))

    return render(request, "recipes/index.html", {
        "recipes": data_transfer_objects
    })


@login_required
def recipe_list(request):
    """Renders the recipe list. Optionally filtered by a contains-textfilter."""
    return render(request, 'recipes/recipelist.html', {
        'recipes': Recipe.objects.all().order_by("name"),
        'textfilter': json.dumps(request.GET.get('q'))
    })


@login_required
def add_recipe(request):
    """Renders the recipe add form."""
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save()
            update_recipe_ingredients(recipe, request.POST.get('ingredients'))

            return HttpResponseRedirect(reverse('recipe_list'))
    else:
        form = RecipeForm()

    return render(request, 'recipes/recipe.html', {
        'mode': 'add',
        'form': form,
        'ingredientsJson': json.dumps([])
    })


@login_required
def edit_recipe(request, recipe_id):
    """Renders the recipe edit form."""
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            update_recipe_ingredients(recipe, request.POST.get('ingredients'))
            form.save()

            return HttpResponseRedirect(reverse('recipe_list'))

    return render(request, 'recipes/recipe.html', {
        'mode': 'edit',
        'context': recipe,
        'form': form if request.method == 'POST' else RecipeForm(instance=recipe),
        'ingredientsJson': json.dumps(list(map(lambda x: {
            "amount": x.amount,
            "unit": x.unit,
            "ingredient": x.ingredient
        }, RecipeIngredient.objects.filter(recipe=recipe))))
    })


@csrf_exempt
def recipe_api(request):
    """Recipe API. Currently, only DELETE is supported."""
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Unauthorized"}, status=401)

    if request.method == "DELETE":
        data = json.loads(request.body)
        if not data.get("id"):
            return JsonResponse({"message": "Id required."}, status=400)

        Recipe.objects.get(pk=data.get("id")).delete()
        return JsonResponse({"message": "Success"}, status=200)

    return JsonResponse({"message": "Method not allowed."}, status=405)


def recipes_api(request, page_no):
    """Returns an (optionally filtered) paginated recipe list."""
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Unauthorized"}, status=401)

    try:
        query_string = request.GET.get("q")
        if query_string is not None:
            recipe_query_set = Recipe.objects.filter(name__contains=query_string)
        else:
            recipe_query_set = Recipe.objects.all()

        paginator = Paginator(recipe_query_set.order_by("name"), settings.RECIPE_ENTRIES_PER_PAGE)
        cur_page = min(page_no, paginator.num_pages)
        page = paginator.page(cur_page)

        recipe_dto_list = to_recipe_data_transfer_objects(page.object_list)

    except EmptyPage:
        return JsonResponse({"message": "Bad request"}, status=400)

    return JsonResponse({
        "recipes": recipe_dto_list,
        "hasNext": page.has_next(),
        "hasPrevious": page.has_previous(),
        "numPages": paginator.num_pages,
        "curPage": cur_page
    }, status=200)


@csrf_exempt
def language_api(request):
    """Changes the session language."""
    if request.method == 'POST':
        data = json.loads(request.body)
        lang_code = data.get("langCode")

        if not lang_code:
            return JsonResponse({"message": "langCode required."}, status=400)

        translation.activate(lang_code)
        response = JsonResponse({"message": f"Language \"{lang_code}\" set."}, status=200)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
        return response

    return JsonResponse({"message": "Method not allowed."}, status=405)


def login_view(request):
    """Login page"""
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "recipes/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "recipes/login.html")


def logout_view(request):
    """Logs the user out and redirects to the index page"""
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    """Allows the user to create an account"""
    # Deactivate adding user in production.
    if not settings.DEBUG:
        return render(request, "recipes/register.html", {"message": "Registration deactivated."})

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "recipes/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "recipes/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "recipes/register.html")
