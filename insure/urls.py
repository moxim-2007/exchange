from django.urls import path
from . import views

urlpatterns = [
    path("create_category/", views.CreateCategory.as_view()),
    path("create_product/", views.CreateProduct.as_view()),
    path("list_product/<str:company>/", views.ListProducts.as_view()),
    path("response/<str:product>/", views.CreateResponse.as_view()),
    path("responses/<str:company>/", views.ListResponses.as_view()),
]
