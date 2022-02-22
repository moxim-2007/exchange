from django.urls import path, re_path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path("create_category/", login_required(views.CreateCategory.as_view())),
    path("create_product/", login_required(views.CreateProduct.as_view())),
    path(
        "delete_product/<str:product>/", login_required(views.DeleteProduct.as_view())
    ),
    path(
        "product_info/<str:product>/", login_required(views.ProductDetail.as_view())
    ),
    re_path(
        r"^list_product/(?P<company>.*)/(?P<query>.*)(?P<filter_name>.*)$",
        views.ListProducts.as_view(),
    ),
    path("response/<str:product>/", views.CreateResponse.as_view()),
    path("responses/<str:company>/", login_required(views.ListResponses.as_view())),
]
