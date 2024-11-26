from django.db import models
from django.contrib.auth.models import AbstractUser, User

from social.models import Community

# Create your models here.

class Profile(models.Model):
    photo = models.ImageField(upload_to='profile_photos/')
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, blank=True)
    about_user = models.TextField(blank=True)

    