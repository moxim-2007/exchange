from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from . import forms
from .models import Category, Product, ProductInfo, Response
from account.models import Company


class CreateCategory(CreateView):
    model = Category
    form_class = forms.CreateCategoryForm
    success_url = "/"
    template_name = "insure/create_object.html"

    def post(self, request, *args, **kwargs):
        category_form = self.form_class(data=request.POST)
        if category_form.is_valid():
            cd = category_form.cleaned_data
            caregory = self.model.objects.create(name=cd["name"])
            caregory.save()
            return redirect("/create_category")

    def get(self, request, *args, **kwargs):
        category_form = self.form_class()
        return render(request, "insure/create_object.html", {"form": category_form})


class CreateProduct(CreateView):
    model = [Product, ProductInfo]
    form_class = forms.CreateCategoryForm
    success_url = "/"
    template_name = "insure/create_object.html"

    def post(self, request, *args, **kwargs):
        product_form = self.form_class(data=request.POST)
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
                price=cd["price"], duration=cd["duration"], product=product
            )
            productInfo.save()
            return redirect("/create_product")

    def get(self, request, *args, **kwargs):
        product_form = self.form_class()
        return render(request, "insure/create_object.html", {"form": product_form})


class CreateResponse(CreateView):
    model = Response
    form_class = forms.CreateResponseForm
    success_url = "/list_product/all"
    template_name = "insure/create_object.html"

    def post(self, request, *args, **kwargs):
        response_form = self.form_class(data=request.POST)
        if response_form.is_valid():
            cd = response_form.cleaned_data
            response = self.model.objects.create(
                full_name=cd["full_name"],
                phone=cd["phone"],
                email=cd["email"],
                product=Product.objects.get(id=self.kwargs["product"]),
            )
            response.save()
            return redirect("/list_product/all")

    def get(self, request, *args, **kwargs):
        response_form = self.form_class()
        return render(request, "insure/create_object.html", {"form": response_form})


class ListProducts(ListView):
    model = ProductInfo
    paginate_by = 10
    template_name = "insure/list_product.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs["company"] != "all":
            company = Company.objects.get(id=self.kwargs["company"])
            products = Product.objects.filter(company=company)
            context["products"] = self.model.objects.filter(product__in=products)
        return context


class ListResponses(ListView):
    model = Response
    paginate_by = 10
    template_name = "insure/list_responses.html"
    context_object_name = "responses"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.get(username=self.request.user.username)
        products = Product.objects.filter(company=company)
        context["responses"] = self.model.objects.filter(product__in=products)
        return context
