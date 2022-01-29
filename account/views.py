from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib import messages

from . import forms


def index(request):
    return render(request, "index.html")


def my_login(request):
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("/")
                else:
                    messages.add_message(request, messages.ERROR, "disabled account")
            else:
                messages.add_message(request, messages.ERROR, "invalid login")
    else:
        form = forms.LoginForm()
    return render(request, "account/login.html", {"form": form})


def register(request):
    if request.method == "POST":
        user_form = forms.RegForm(data=request.POST, files=request.FILES)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            cd = user_form.cleaned_data
            new_user.set_password(cd["password"])
            new_user.save()
            user = authenticate(username=cd["username"], password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("/")
            return redirect("/")
    else:
        user_form = forms.RegForm()
        return render(request, "account/register.html", {"user_form": user_form})


def my_logout(request):
    logout(request)
    return redirect("/")


@login_required
def edit(request):
    if request.method == "POST":
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

    else:
        user_form = forms.UserEditForm(instance=request.user)
        return render(
            request,
            "account/edit.html",
            {"user_form": user_form},
        )
    return redirect("/")
