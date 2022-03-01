from django.urls import path, re_path
from django.contrib.auth.decorators import login_required

from views import (
    CreateResponse,
    CreateCategory,
    CreateProduct,
    DeleteProduct,
    ProductDetail,
    ListProducts,
    ListResponses,
)

urlpatterns = [
    path("create_category/", login_required(CreateCategory.as_view())),
    path("create_product/", login_required(CreateProduct.as_view())),
    path("delete_product/<str:product>/", login_required(DeleteProduct.as_view())),
    path("product_info/<str:product>/", ProductDetail.as_view()),
    re_path(
        r"^list_product/(?P<company>.*)/(?P<query>.*)(?P<filter_name>.*)$",
        ListProducts.as_view(),
    ),
    path("response/<str:product>/", CreateResponse.as_view()),
    path("responses/<str:company>/", login_required(ListResponses.as_view())),
]
