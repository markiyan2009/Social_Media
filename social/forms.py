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

class CommunitiesFilterForm(forms.Form):
    filter = forms.CharField(required=False, label='Filter')

    def __init__(self, *args, **kwargs):
        super(CommunitiesFilterForm, self).__init__(*args, **kwargs)
        self.fields["filter"].widget.attrs.update({"class": "form-control", 'id':'filter_communities', 'name' : "filter_communities" })