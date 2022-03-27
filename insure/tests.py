from django.test import TestCase, Client
from django.core.management import call_command

from .services import get_count_visit
from .models import Product
from exchange.settings import DATABASES


class ListProductTestCase(TestCase):
    databases = DATABASES
    url = "/list_product/all/"

    def setUp(self) -> None:
        call_command("loaddata", "fixtures/initial_data.json")
        self.client = Client()

    def test_TemplateUsed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "insure/list_product.html")

    def test_pagination(self):
        response = self.client.get(self.url)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertTrue(len(response.context["products"]) == 10)

    def test_list_all_products(self):
        products = Product.objects.all()
        response = self.client.get(f"{self.url}?page={len(products) // 10 + 1}")
        self.assertEqual(len(response.context["products"]), len(products) % 10)

    def test_search(self):
        url = "/list_product/all/?query=дом"
        response = self.client.get(url)
        self.assertEqual(len(response.context["products"]), 3)

    def test_filtration(self):
        url = "/list_product/all/?filter=name"
        response = self.client.get(url)
        self.assertEqual(response.context["products"][0].name, "легковой автомобиль")
        self.assertEqual(response.context["products"][9].name, "картон")


class ProductDetailTestCase(TestCase):
    databases = DATABASES
    url = f"/product_info/"

    def setUp(self) -> None:
        call_command("loaddata", "fixtures/initial_data.json")
        self.client = Client()

    def test_TemplateUsed(self):
        product = Product.objects.get(name="яблоко")
        response = self.client.get(f"{self.url}{product.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "insure/product_detail.html")

    def test_productinfo(self):
        product = Product.objects.get(name="яблоко")
        response = self.client.get(f"{self.url}{product.id}/")
        self.assertEqual(response.context["object"].product, product)

    def test_countvisut(self):
        product = Product.objects.get(name="яблоко")
        response = self.client.get(f"{self.url}{product.id}/")
        self.assertEqual(
            get_count_visit(str(response.context["object"].product.id)),
            get_count_visit(str(product.id)),
        )
