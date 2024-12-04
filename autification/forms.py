from django import forms
from autification import models
from django.contrib.auth.models import User
from .models import Profile

class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name','photo', 'about_user']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'name','about_user']
        fields['photo'].required  = False
        fields['name'].required = False
        fields['about_user'].required = False
