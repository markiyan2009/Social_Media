from django.shortcuts import render
from autification.models import Profile
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

# Create your views here

class CustomLoginView(LoginView):
    template_name = 'autification/login.html'
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page="login"