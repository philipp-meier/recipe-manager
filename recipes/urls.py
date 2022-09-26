from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),

    path("recipe/add", views.add_recipe, name="add_recipe"),
    path("recipe/edit/<int:recipe_id>", views.edit_recipe, name="edit_recipe"),
    path("recipe/list", views.recipe_list, name="recipe_list"),

    path("api/v1/recipe", views.recipe_api, name="recipe_api"),
    path("api/v1/recipes/<int:page_no>", views.recipes_api, name="recipes_api"),
    path("api/v1/language", views.language_api, name="language_api"),
]
