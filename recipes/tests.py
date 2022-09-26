import json
from django.test import Client, TestCase
from .models import User, Recipe, RecipeCategory

test_recipes = ["Pizza", "French Toast", "Spaghetti", "Waffles", "Brownies"]


class RecipeApiTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="user", password="secret")

        # Main category
        category = RecipeCategory.objects.create(name="Main dish")
        category.save()

        # Test recipes
        for recipe in test_recipes:
            Recipe.objects.create(name=recipe, category=category).save()

    def test_is_protected(self):
        response = self.client.get("/api/v1/recipes/1")
        self.assertEqual(response.status_code, 401)

        self.client.login(username="user", password="secret")
        response = self.client.get("/api/v1/recipes/1")
        self.assertEqual(response.status_code, 200)

    def test_api_result(self):
        self.client.login(username="user", password="secret")
        response = self.client.get("/api/v1/recipes/1")
        result = response.json()

        self.assertTrue("recipes" in result)
        self.assertTrue("hasNext" in result)
        self.assertTrue("hasPrevious" in result)
        self.assertTrue("numPages" in result)
        self.assertTrue("curPage" in result)

    def test_api_result_filtered(self):
        self.client.login(username="user", password="secret")
        search_param = "Piz"
        response = self.client.get(f"/api/v1/recipes/1?q={search_param}")
        result = response.json()

        for recipe in result["recipes"]:
            self.assertTrue(search_param in recipe["name"])
