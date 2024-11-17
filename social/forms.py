from django.forms.models import ModelForm
from social.models import Comment, Post, Discusion,Community
from django import forms

class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'post_html']
        widgets = {
            'post_html' : forms.Textarea(attrs = {'class':'form-control', 'id':'editor'})
        }

class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']