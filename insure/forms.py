from django import forms

from .models import Category


class CreateCategoryForm(forms.Form):
    name = forms.CharField(label="Name of category")


class CreateProductForm(forms.Form):
    name = forms.CharField(label="Name of product:")
    description = forms.CharField(label="Description:")
    category = forms.ChoiceField(
        label="Category of product:",
        choices=[(category.name, category.name) for category in Category.objects.all()],
    )
    price = forms.IntegerField(label="Price of product:")
    duration = forms.IntegerField(label="Duration (month) of insurance:")


class CreateResponseForm(forms.Form):
    full_name = forms.CharField(label="Your fullname")
    phone = forms.CharField(label="Your phone")
    email = forms.CharField(label="Your email")
