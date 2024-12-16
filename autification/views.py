from typing import Any, Dict, List, Optional, Type
from django import http
from django.forms.forms import BaseForm
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from autification.models import Profile
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from social.models import Community
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import ProfileCreateForm, ProfileUpdateForm
from django import forms

# Create your views here

class CustomLoginView(LoginView):
    template_name = 'autification/login.html'
    redirect_authenticated_user = True
 

    def get_form(self, form_class = None ):
        form = super().get_form(form_class)
        form.fields['username'].widget = forms.TextInput(attrs = {'class' : 'form-control'})
        form.fields['password'].widget = forms.PasswordInput(attrs={'class' : 'form-control'})
        return form
    


    
class ProfileDetailView(DetailView):
    
    template_name = 'autification/profile_detail.html'
    model = Profile
    context_object_name = 'profile'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['communities'] = self.request.user.subscribers.all()

        profile = Profile.objects.filter(user = self.request.user).first()
        
        context['profile'] = profile
        return context
        

class RegisterView(CreateView):
    template_name = 'autification/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)
    
    def get_form(self, form_class = None):
        form = super().get_form(form_class)
        form.fields['username'].widget = forms.TextInput(attrs = {'class' : 'form-control'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class' : 'form-control'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class' : 'form-control'})
        return form

class ProfileCreateView(CreateView):
    form_class = ProfileCreateForm
    template_name = 'autification/profile_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
            

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('communities')
    
class ProfileUpdateView(UpdateView):
    form_class = ProfileUpdateForm
    model = Profile
    template_name = 'autification/profile_update.html'

    def get_success_url(self):
        return reverse_lazy('communities')

