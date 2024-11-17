from typing import Any, Dict
from django import http
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from social.models import Comment, Community, Post, Discusion, Genre
from django.views.generic import ListView, DeleteView, DetailView, UpdateView, View, CreateView
from social.forms import PostCreateForm, CommentCreateForm
from django.urls import reverse_lazy, reverse
from autification.models import Profile
from django.http import JsonResponse, HttpResponseRedirect



class ComunitiesListView(ListView):
    model = Community
    template_name = 'social/communities_list.html'
    context_object_name = 'communities'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        # fiter_input = self.kwargs['filter_communities']

        # communities = Community.objects.filter(genres = fiter_input).first()
        # context['communities'] = communities
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

class PostCreateView(CreateView):
    form_class = PostCreateForm
    template_name = 'social/post_create.html'

    def get_success_url(self):
        return  reverse_lazy('community', kwargs ={'pk' : self.kwargs['community_pk']})
    
    def form_valid(self, form):
        form.instance.community = Community.objects.filter(pk = self.kwargs['community_pk']).first()
        return super().form_valid(form)
    
class LikePostView(View):
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
    
class LikeCommentView(View):
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

