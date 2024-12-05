from typing import Any, Dict, Optional
from django import http
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from social.models import Comment, Community, Post, Discusion, Genre
from django.views.generic import ListView, DeleteView, DetailView, UpdateView, View, CreateView
from social.forms import PostCreateForm, CommentCreateForm, DiscusionCreateForm, CommunitiesFilterForm
from django.urls import reverse_lazy, reverse
from autification.models import Profile
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import IsSubscriberMixin, IsSubscriberFormsMixin
from django.shortcuts import get_object_or_404 



class ComunitiesListView(ListView):
    model = Community
    template_name = 'social/communities_list.html'
    context_object_name = 'communities'
    paginate_by = 5

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        # fiter_input = self.kwargs['filter_communities']

        communities = Community.objects.all()
        
        query = int(self.request.GET.get('page','1'))
        print(query)

        filter_community = self.request.GET.get("filter", "")
        if filter_community:
            comunity_filter = Community.objects.filter(genres__name = filter_community).all()
            context['communities'] = comunity_filter

        else:
            context['communities'] = Community.objects.all()
        

        context['communities'] = context['communities'][(query*5) -5 :query*5]
        
        context["form"] = CommunitiesFilterForm(self.request.GET)

        
        if self.request.user.is_authenticated:
            context['profile'] = Profile.objects.filter(user = self.request.user).first()
            
        return context


class SearchCommunitiesView(View):
    def get(self, request):
        
        query = request.GET.get('query', '')
        
        if query:
            results = Genre.objects.filter(name__icontains=query)[:10]  
            data = [{'name' : item.name} for item in results]
        else:
            data = []

        return JsonResponse({"results": data})

class CommunityDetailView(IsSubscriberMixin ,DetailView):
    model = Community
    template_name = 'social/community_detail.html'
    context_object_name = 'community'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        community = context['community']
        context['profile'] = Profile.objects.filter(user = self.request.user).first()
        context['posts'] = community.post_set.all()
        context['discusions'] = community.discusion_set.all()

        return context
class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post
    template_name = 'social/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['community'] = context['post'].community
        return context
    
class DiscusionDetailView(LoginRequiredMixin ,DetailView):
    model = Discusion
    template_name = 'social/discusion_detail.html'
    context_object_name = 'discusion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = context['discusion'].comments.all()
        
        context['comment_form'] = CommentCreateForm()
        
        return context
    
    
    def post(self, request, *args, **kwargs):
        comment_form = CommentCreateForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.discusion = self.get_object()
            comment.save()

            return redirect('discusion', pk=comment.discusion.pk)

class PostCreateView(IsSubscriberFormsMixin ,CreateView):
    form_class = PostCreateForm
    template_name = 'social/post_create.html'

    def get_success_url(self):
        return  reverse_lazy('community', kwargs ={'pk' : self.kwargs['community_pk']})
    
    def form_valid(self, form):
        form.instance.community = Community.objects.filter(pk = self.kwargs['community_pk']).first()
        return super().form_valid(form)
    
class LikePostView(LoginRequiredMixin ,View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.filter(pk = pk).first()
        
        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        
        if not is_like:
            post.likes.add(request.user)
        if is_like:
            post.likes.remove(request.user)
        
        print(post.likes.count)
        return HttpResponseRedirect(reverse_lazy('post_detail', kwargs={'pk' : post.pk}))
    
class LikeCommentView(LoginRequiredMixin,View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.filter(pk = pk).first()
        discusion = comment.discusion 
        
        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break
        
        if not is_like:
            comment.likes.add(request.user)
        if is_like:
            comment.likes.remove(request.user)
        
        
        return HttpResponseRedirect(reverse_lazy('discusion', kwargs={'pk' : discusion.pk}))

class SubscribeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        community = Community.objects.filter(pk = self.kwargs['community_pk']).first()
        print(community)
        is_subscribe = False
        print(community.subscribers)
        for subscribe in community.subscribers.all():
            if subscribe == request.user:
                is_subscribe = True
                break
        if not is_subscribe:
            community.subscribers.add(request.user)
        if is_subscribe:
            community.subscribers.remove(request.user)

        return HttpResponseRedirect(reverse_lazy('communities'))
    
class DiscucsionCreateView(IsSubscriberFormsMixin, CreateView):
    form_class = DiscusionCreateForm
    template_name = 'social/discusion_create.html'
    

    def get_success_url(self):
        return  reverse_lazy('community', kwargs ={'pk' : self.kwargs['community_pk']})

    def form_valid(self, form):
        community = Community.objects.filter(pk =self.kwargs['community_pk']).first()
        author = self.request.user
        form.instance.community = community
        form.instance.author = author
        return super().form_valid(form)
    
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'social/post_delete.html'

    def get_success_url(self) -> str:
        return reverse_lazy('community', kwargs = {'pk' : self.kwargs['community_pk']})
    
    def get_object(self, queryset = None):
        post = Post.objects.filter(pk = self.kwargs['post_pk']).first()

        return post
    
    
class PostUpdateView(UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'social/post_update.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('community', kwargs = {'pk' : self.kwargs['community_pk']})
    
    def get_object(self, queryset = None):
        post = Post.objects.filter(pk = self.kwargs['post_pk']).first()

        return post
    


class DiscusionDeleteView(DeleteView):
    model = Discusion
    template_name = 'social/discusion_delete.html'

    def get_success_url(self) -> str:
        return reverse_lazy('community', kwargs = {'pk' : self.kwargs['community_pk']})
    
    def get_object(self, queryset = None):
        discusion = Discusion.objects.filter(pk = self.kwargs['discusion_pk']).first()

        return get_object_or_404(Discusion, pk=self.kwargs['discusion_pk']) 
    
    
    