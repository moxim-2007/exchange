from django.urls import path
from django.conf.urls.static import static
from exchange import settings
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("login/", views.CompanyLogin.as_view(), name="login"),
    path("register/", views.CompanyRegister.as_view(), name="register"),
    path("logout/", views.CompanyLogout.as_view(), name="logout"),
    path("edit/", views.CompanyEdit.as_view(), name="edit"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
