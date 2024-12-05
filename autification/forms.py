from django import forms
from autification import models
from django.contrib.auth.models import User
from .models import Profile

class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name','photo', 'about_user']
        
class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['photo'].required  = False
        self.fields['name'].required = False
        self.fields['about_user'].required = False


    class Meta:
        model = Profile
        fields = ['photo', 'name','about_user']
    
        