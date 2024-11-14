from typing import Any, Dict
from django import http
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from social.models import Comment, Community, Post, Discusion, Genre
from django.views.generic import ListView, DeleteView, DetailView, UpdateView, View, CreateView
from social.forms import PostCreateForm
from django.urls import reverse_lazy
from autification.models import Profile
from django.http import JsonResponse


class ComunitiesListView(ListView):
    model = Community
    template_name = 'social/communities_list.html'
    context_object_name = 'communities'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        
        context['profile'] = Profile.objects.filter(user = self.request.user).first()
        return context


class SearchCommunitiesView(View):
    def get(self, request):
        
        query = request.GET.get('query', '')
        print(query)
        if query:
            results = Genre.objects.filter(name__icontains=query)[:10]  
            data = [{'name' : item.name} for item in results]
        else:
            data = []

        return JsonResponse({"results": data})

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
    
