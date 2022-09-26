import json
from .models import RecipeIngredient


def update_recipe_ingredients(recipe, ingredients_json):
    # Remove old ingredients
    RecipeIngredient.objects.filter(recipe=recipe).delete()

    # Add new ingredients
    ingredients = json.loads(ingredients_json)
    for ingredient in ingredients:
        RecipeIngredient(recipe=recipe,
                         ingredient=ingredient["ingredient"],
                         amount=ingredient["amount"],
                         unit=ingredient["unit"]).save()


def to_recipe_data_transfer_objects(recipes):
    return list(map(lambda recipe: {
        "pk": recipe.pk,
        "name": recipe.name,
        "category": recipe.category.name,
        "img": recipe.photo.url if recipe.photo else None,
    }, recipes))
