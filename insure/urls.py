from django.urls import path
from . import views

urlpatterns = [
    path("create_category/", views.create_category),
    path("create_product/", views.create_product),
]
