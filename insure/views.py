from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from datetime import datetime

from . import forms
from .models import Category, Product, ProductInfo, Response
from account.models import Company
from .services import search_product, add_page_visit, get_count_visit
from .tasks import send_response_notification


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
    form_class = forms.CreateProductForm
    success_url = "/"
    template_name = "insure/create_object.html"

    def post(self, request, *args, **kwargs):
        product_form = self.form_class(data=request.POST)
        if product_form.is_valid():
            cd = product_form.cleaned_data
            product = Product.objects.create(
                name=cd["name"],
                category=Category.objects.get(name=cd["category"]),
                company=Company.objects.get(username=request.user.username),
            )
            product.save()
            productInfo = ProductInfo.objects.create(
                description=cd["description"],
                price=cd["price"],
                duration=cd["duration"],
                product=product,
            )
            productInfo.save()
            return redirect("/create_product")

    def get(self, request, *args, **kwargs):
        product_form = self.form_class()
        return render(request, "insure/create_object.html", {"form": product_form})


class DeleteProduct(DeleteView):
    model = Product
    template_name = "insure/confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        productinfo = ProductInfo.objects.get(product=self.object)
        success_url = self.get_success_url()
        productinfo.delete()
        self.object.delete()
        return redirect(success_url)

    def get_success_url(self):
        return f"/list_product/{self.object.company.id}"

    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.kwargs["product"])


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
            send_response_notification.delay(
                {
                    "email": response.email,
                    "phone": response.phone,
                    "full_name": response.full_name,
                    "company": response.product.company.name,
                    "product": response.product.name,
                    "response_date": datetime.now(),
                }
            )
            return redirect("/list_product/all")

    def get(self, request, *args, **kwargs):
        response_form = self.form_class()
        return render(request, "insure/create_object.html", {"form": response_form})


class ListProducts(ListView):
    model = Product
    template_name = "insure/list_product.html"
    paginate_by = 10
    context_object_name = "products"

    def get_queryset(self):
        query = self.request.GET.get("query")
        company_id = self.kwargs["company"]
        queryset = self.model.objects.all()
        if company_id != "all":
            company = Company.objects.get(id=company_id)
            queryset = self.model.objects.filter(company=company)
        result = []
        for q in search_product(query, self.request.GET.get("filters")):
            for product in queryset:
                if product == q:
                    result.append(product)
        return result


class ProductDetail(DetailView):
    model = ProductInfo
    template_name = "insure/product_detail.html"

    def get_object(self, queryset=None):
        product = Product.objects.get(id=self.kwargs["product"])
        return self.model.objects.get(product=product)

    def get_context_data(self, **kwargs):
        add_page_visit(self.kwargs["product"])
        context = super().get_context_data(**kwargs)
        if self.request.user.id == self.object.product.company.id:
            context["count_visit"] = int(get_count_visit(str(self.object.product.id)))
        return context


class ListResponses(ListView):
    model = Response
    paginate_by = 10
    template_name = "insure/list_responses.html"
    context_object_name = "responses"

    def get_queryset(self):
        company = Company.objects.get(username=self.request.user.username)
        products = Product.objects.filter(company=company)
        queryset = self.model.objects.filter(product__in=products)
        return queryset
