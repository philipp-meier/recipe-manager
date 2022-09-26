from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class RecipeCategory(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=128)
    photo = models.ImageField(upload_to='recipes/', blank=True, null=True)
    description = models.TextField(max_length=4096, blank=True, null=True)
    category = models.ForeignKey(RecipeCategory, on_delete=models.CASCADE, related_name="recipes")

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.CharField(max_length=128)
    amount = models.CharField(max_length=32)
    unit = models.CharField(max_length=32)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
