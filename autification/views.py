from typing import Any, Dict, List
from django import http
from django.shortcuts import render
from autification.models import Profile
from django.views.generic import CreateView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

# Create your views here

class CustomLoginView(LoginView):
    template_name = 'autification/login.html'
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = 'login'
    
class ProfileDetailView(DetailView):
    template_name = 'autification/profile_detail.html'
    model = Profile
    context_object_name = 'profile'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(user = self.request.user).first()
        return context
    