from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.

class Community(models.Model):
    name = models.CharField(max_length=50)
    GENRES_STATUS =[
        ['games','Games'],
        ['films','Films'],
        ['programing','Programing'],
        ['sport','Sport'],
        ['fishing','Fishing'],

    ]
    genres = models.CharField(choices=GENRES_STATUS, max_length=40)
    author = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class Discusion(models.Model):
    topic = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete= models.PROTECT)
    community = models.ForeignKey(Community, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.author.username

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete= models.PROTECT)
    text = models.TextField()
    likes = models.IntegerField()
    discusion = models.ForeignKey(Discusion,on_delete= models.PROTECT, related_name='comments')
    
    def __str__(self):
        return self.author

class Post(models.Model):
    name = models.CharField(max_length=50)
    post_html = HTMLField()
    community = models.ForeignKey(Community, on_delete=models.PROTECT, null=True)
    def __str__(self):
        return self.name