from typing import Any, Dict
from django import http
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from social.models import Comment, Community, Post, Discusion
from django.views.generic import ListView, DeleteView, DetailView, UpdateView, View, CreateView
from social.forms import PostCreateForm
from django.urls import reverse_lazy


class ComunitiesListView(ListView):
    model = Community
    template_name = 'social/communities_list.html'
    context_object_name = 'communities'

class CommunityDetailView(DetailView):
    model = Community
    template_name = 'social/community_detail.html'
    context_object_name = 'community'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        community = context['community']
        context['posts'] = community.post_set.all()
        context['discusions'] = community.discusion_set.all()

        return context
class PostDetailView(DetailView):
    model = Post
    template_name = 'social/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['community'] = context['post'].community
        return context
    
class DiscusionDetailView(DetailView):
    model = Discusion
    template_name = 'social/discusion_detail.html'
    context_object_name = 'discusion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = context['discusion'].comments.all()
        return context

class PostCreateView(CreateView):
    form_class = PostCreateForm
    template_name = 'social/post_create.html'

    def get_success_url(self):
        return  reverse_lazy('community', kwargs ={'pk' : self.kwargs['community_pk']})
    
    def form_valid(self, form):
        form.instance.community = Community.objects.filter(pk = self.kwargs['community_pk']).first()
        return super().form_valid(form)
    
