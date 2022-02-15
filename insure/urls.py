from django.urls import path, re_path
from . import views

urlpatterns = [
    path("create_category/", views.CreateCategory.as_view()),
    path("create_product/", views.CreateProduct.as_view()),
    re_path(
        r"^list_product/(?P<company>.*)/(?P<query>.*)(?P<filter_name>.*)$", views.ListProducts.as_view()
    ),
    path("response/<str:product>/", views.CreateResponse.as_view()),
    path("responses/<str:company>/", views.ListResponses.as_view()),
]
