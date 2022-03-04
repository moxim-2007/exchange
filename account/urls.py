from django.urls import path
from django.conf.urls.static import static
from exchange import settings
from .views import HomeView, CompanyLogin, CompanyEdit, CompanyRegister, CompanyLogout, CompanyDetail

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", CompanyLogin.as_view(), name="login"),
    path("register/", CompanyRegister.as_view(), name="register"),
    path("logout/", CompanyLogout.as_view(), name="logout"),
    path("edit/", CompanyEdit.as_view(), name="edit"),
    path("company_info/<str:company>/", CompanyDetail.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
