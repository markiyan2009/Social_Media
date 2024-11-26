from django import forms
from autification import models
from django.contrib.auth.models import User
from .models import Profile

class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name','photo', 'about_user']