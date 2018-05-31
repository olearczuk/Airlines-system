"""Module for user authentication"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from system.authentication.forms import RegistrationForm, LoginForm


@login_required
def logout_view(request):
    """Logout view"""
    logout(request)
    return redirect(to="/")


def login_user(request):
    """Login view"""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST["username"],
                                password=request.POST["password"])
            if user is not None:
                login(request, user)
                return redirect(to="/flights/flights_list")
        else:
            print(form.errors)
    form = LoginForm()
    return render(request, template_name="login.html", context=locals())


def register_view(request):
    """Register view"""
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create(**form.cleaned_data)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect(to='/auth/login/')
    form = RegistrationForm()
    return render(request, template_name="register.html", context=locals())
