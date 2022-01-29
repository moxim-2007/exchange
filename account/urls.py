from django.urls import path
from django.conf.urls.static import static
from exchange import settings
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.my_login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.my_logout, name="logout"),
    path("edit/", views.edit, name="edit"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
