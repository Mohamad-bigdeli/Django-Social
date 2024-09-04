from django.db.models import Count , Q
from django.db.models.base import Model as Model
from django.forms import BaseModelForm
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from .models import *
from taggit.models import Tag
from .forms import *
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
# from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Create your views here.

@login_required
@require_POST
def comment_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    user = request.user
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = user
        comment.save()
    form = CommentForm()
    context = {
        'post':post,
        'comment':comment,
        'form':form
    }
    return render(request, 'forms/comment.html', context)


def post_search(request): 
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # result1 = Post.objects.annotate(similarity=TrigramSimilarity('author', query)).filter(similarity__gt=0.1).order_by('-similarity')
            # result2 = Post.objects.annotate(similarity=TrigramSimilarity('caption', query)).filter(similarity__gt=0.1).order_by('-similarity')
            results = Post.objects.filter(Q(author__username__icontains=query)).all() | Post.objects.filter(Q(caption__icontains=query)).all()
    context = { 
        'query' : query,
        'results' : results
}
    return render(request, 'social/search.html', context)

class HomeView(ListView):
    template_name = 'social/post_list.html'
    model = Post
    context_object_name = "posts"

    def get_queryset(self):
        if 'tag_slug' in self.kwargs:    
            tag_slug = self.kwargs['tag_slug']
            tag = get_object_or_404(Tag, slug=tag_slug)
            return Post.objects.filter(tags__in=[tag])
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'tag_slug' in self.kwargs:
            tag = self.kwargs['tag_slug']
            context['tag'] = tag
        return context

    
class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post
    template_name = 'social/post_detail.html'
    login_url = reverse_lazy('account:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            post = get_object_or_404(Post, id=self.kwargs['pk'])
            post_tags_ids = post.tags.values_list('pk', flat=True)
            similar_posts = Post.objects.filter(tags__in = post_tags_ids).exclude(id=post.id)
            similar_posts = similar_posts.annotate(same_tags = Count('tags')).order_by('-same_tags', '-created')[:2]
            context['similar_posts'] = similar_posts
            context['comments'] = post.comments.all()
            context['comment_form'] = CommentForm()
        return context

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'social/profile.html'
    login_url = reverse_lazy('account:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        posts = Post.objects.filter(author=user).all()
        context['user'] = user
        context['posts'] = posts
        return context
    
class CreatePostView(LoginRequiredMixin,CreateView):
    form_class = CreatePostForm
    template_name = 'forms/create_post.html'
    login_url = reverse_lazy('account:login')
    success_url = reverse_lazy('social:profile')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        image_file = self.request.FILES.get('image')
        if image_file:
            Image.objects.create(image_file=image_file, post=post)
        return super().form_valid(form)

@login_required  
def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method=='POST':
        post.delete()
        return redirect('social:home')
    return render(request, 'forms/delete_post.html', {'post':post})
