from django import forms

from .models import Category


class CreateCategoryForm(forms.Form):
    name = forms.CharField(label="Name of category")


class CreateProductForm(forms.Form):
    name = forms.CharField(label="Name of product:")
    description = forms.CharField(label="Description:")
    category = forms.ChoiceField(
        label="Rating of movie:",
        choices=[(category.name, category.name) for category in Category.objects.all()],
    )
    price = forms.IntegerField(label="Price of product:")
    duration = forms.DurationField(label="Duration of insurance:")
