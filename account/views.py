from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.detail import DetailView

from . import forms
from .models import Company


class HomeView(TemplateView):
    template_name = "index.html"


class CompanyLogin(LoginView):
    template_name = "account/login.html"
    next_page = "/"


class CompanyLogout(LogoutView):
    next_page = "/"


class CompanyRegister(CreateView):
    model = Company
    form_class = forms.RegForm
    success_url = "/"
    template_name = "account/register.html"

    def post(self, request, *args, **kwargs):
        user_form = self.form_class(data=request.POST, files=request.FILES)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            cd = user_form.cleaned_data
            new_user.set_password(cd["password"])
            new_user.save()
            user = authenticate(username=cd["username"], password=cd["password"])
            if user and user.is_active:
                login(request, user)
                return redirect("/")

    def get(self, request, *args, **kwargs):
        return render(request, "account/register.html", {"user_form": self.form_class})


class CompanyEdit(UpdateView):
    model = Company
    form_class = forms.UserEditForm
    success_url = "/"
    template_name = "account/edit.html"
    template_name_suffix = "_update_form"

    def post(self, request, *args, **kwargs):
        user_form = forms.UserEditForm(
            instance=request.user, data=request.POST, files=request.FILES
        )

        if user_form.is_valid():
            old_password = user_form.cleaned_data["old_password"]
            new_password = user_form.cleaned_data["new_password"]
            repeat_password = user_form.cleaned_data["repeat_password"]
            if (
                    check_password(old_password, request.user.password)
                    and new_password == repeat_password
                    and old_password != new_password
            ):
                request.user.set_password(new_password)
            else:
                messages.add_message(request, messages.ERROR, "Password incorrect")
                return render(
                    request,
                    "account/edit.html",
                    {"user_form": user_form},
                )
            user_form.save()
            if "image" in request.FILES:
                user_form.image = request.FILES["image"]
                user_form.save()
            return redirect("/")

    def get(self, request, *args, **kwargs):
        user_form = forms.UserEditForm(instance=request.user)
        return render(
            request,
            "account/edit.html",
            {"user_form": user_form},
        )


class CompanyDetail(DetailView):
    model = Company
    template_name = "account/company_detail.html"

    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.kwargs["company"])
