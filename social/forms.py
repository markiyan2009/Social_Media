from django.forms.models import ModelForm
from social.models import Comment, Post, Discusion,Community
from django import forms
from tinymce.widgets import TinyMCE


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'post_html']
        widgets = {'post_html': TinyMCE(attrs={'cols': 80, 'rows': 30})}

class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class DiscusionCreateForm(ModelForm):
    class Meta:
        model = Discusion
        fields = ['topic']

