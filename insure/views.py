from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from . import forms
from .models import Category, Product, ProductInfo
from account.models import Company


@login_required
def create_category(request):
    if request.method == "POST":
        category_form = forms.CreateCategoryForm(data=request.POST)
        if category_form.is_valid():
            cd = category_form.cleaned_data
            caregory = Category.objects.create(name=cd["name"])
            caregory.save()
    else:
        category_form = forms.CreateCategoryForm()
    return render(request, "insure/create_object.html", {"form": category_form})


@login_required
def create_product(request):
    if request.method == "POST":
        product_form = forms.CreateProductForm(data=request.POST)
        if product_form.is_valid():
            cd = product_form.cleaned_data
            product = Product.objects.create(
                name=cd["name"],
                description=cd["description"],
                category=Category.objects.get(name=cd["category"]),
                company=Company.objects.get(username=request.user.username),
            )
            product.save()
            productInfo = ProductInfo.objects.create(
                price=cd["price"],
                duration=cd["duration"],
                product=product
            )
            productInfo.save()
    else:
        product_form = forms.CreateProductForm()
    return render(request, "insure/create_object.html", {"form": product_form})
