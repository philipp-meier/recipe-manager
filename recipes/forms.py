from django.forms import ModelForm, TextInput, Select, FileInput, Textarea
from django.utils.translation import gettext_lazy as _
from .models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ["name", "category", "photo", "description"]
        labels = {
            "name": _("Name"),
            "category": _("Category"),
            "photo": _("Photo"),
            "description": _("Description")
        }

        # Add bootstraps "form-control" to all widgets
        control_attrs = {"class": "form-control mb-3"}
        widgets = {
            "name": TextInput(attrs=control_attrs),
            "category": Select(attrs=control_attrs),
            "photo": FileInput(attrs=control_attrs),
            "description": Textarea(attrs=control_attrs)
        }
