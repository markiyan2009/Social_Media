from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name
class Community(models.Model):
    name = models.CharField(max_length=50)
    
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    subscribers = models.ManyToManyField(User,  blank=True, related_name='subscribers')

    def __str__(self):
        return self.name

class Discusion(models.Model):
    topic = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete= models.PROTECT, null = True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.author.username

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete= models.PROTECT)
    text = models.TextField()
    likes = models.ManyToManyField(User, blank=True, related_name='likes_comment')
    discusion = models.ForeignKey(Discusion,on_delete= models.PROTECT, related_name='comments')
    
    def __str__(self):
        return self.author

class Post(models.Model):
    name = models.CharField(max_length=50)
    post_html = HTMLField()
    community = models.ForeignKey(Community, on_delete=models.CASCADE, null=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes_post')
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    def __str__(self):
        return self.name