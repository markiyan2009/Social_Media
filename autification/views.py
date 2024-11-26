from typing import Any, Dict, List
from django import http
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from autification.models import Profile
from django.views.generic import CreateView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from social.models import Community
from django.contrib.auth.forms import UserCreationForm
from .forms import ProfileCreateForm

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
        context['communities'] = self.request.user.subscribers.all()
        
        profile = Profile.objects.filter(user = self.request.user).first()
        
        context['profile'] = profile
        

class RegisterView(CreateView):
    template_name = 'autification/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)

class ProfileCreateView(CreateView):
    form_class = ProfileCreateForm
    template_name = 'autification/profile_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        # if not form.instance.photo:
            

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('communities')