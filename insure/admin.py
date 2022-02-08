from django.contrib import admin

from .models import Category, Product, ProductInfo, Response

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductInfo)
admin.site.register(Response)
