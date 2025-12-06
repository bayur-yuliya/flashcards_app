from django.contrib.auth import login
from django.shortcuts import render, redirect

from accounts.forms import CustomUserCreationForm, CustomAuthenticationForm


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("categories_list")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("categories_list")
    form = CustomAuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})
