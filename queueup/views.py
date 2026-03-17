import uuid
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from .igdb import fetch_game_data, get_game_suggestions

from .forms import CreatePost
from .models import Post, JoinRequest
from django.contrib.auth.decorators import login_required
from . import forms
from django.db.models import Q

#Diako Search Feature
from django.db.models import Q

def home(request):
    return render(request, 'home.html')

def tutorial(request):
    return render(request, 'tutorial.html')

def about(request):
    return render(request, 'about.html')

def posts_list(request):
    query = request.GET.get('q')

    posts = Post.objects.all()

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(author__username__icontains=query)
        )

    return render(request, 'posts/posts_list.html', {
        'posts': posts,
        'query': query
    })


def post_page(request, slug):
    post = get_object_or_404(Post, slug=slug)
    has_applied = False
    if request.user.is_authenticated:
        has_applied = JoinRequest.objects.filter(post=post, applicant=request.user).exists()

    if request.method == 'POST':
        form = forms.JoinRequestForm(request.POST)

        if form.is_valid() and not has_applied and request.user != post.author:
            join_request = form.save(commit=False)
            join_request.post = post
            join_request.applicant = request.user
            join_request.save()

            return redirect(request.path_info)
    else:
        form = forms.JoinRequestForm()

    return render(request, 'posts/post_page.html', {
        'post': post,
        'form': form,
        'has_applied': has_applied
    })

@login_required(login_url='/users/login/')
def post_new(request):
    if request.method == 'POST':
        form = forms.CreatePost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            unique_id = uuid.uuid4().hex[:6]
            post.slug = f"{slugify(post.title)}-{unique_id}"

            game_search_query = form.cleaned_data.get('game_name')
            if game_search_query:
                game_data = fetch_game_data(game_search_query)
                if game_data:
                    post.game_name = game_data['name']
                    post.cover_url = game_data['cover_url']
                    post.banner_url = game_data['banner_url']

            post.save()
            return redirect('posts:list')
    else:
        form = CreatePost()
    return render(request, 'posts/post_new.html', {'form': form})

@login_required
def my_posts_view(request):
    user_posts = Post.objects.filter(author=request.user).order_by('-date')
    return render(request, 'posts/my_posts.html', {'posts': user_posts})

@login_required(login_url='/users/login/')
def lobby_view(request, lobby_name):
    post = get_object_or_404(Post, slug=lobby_name)
    messages = post.messages.all()[:50]
    return render(request, 'queueup/lobby.html', {
        'post': post,
        'lobby_name': lobby_name,
        'messages': messages
    })

def api_search_games(request):
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'results': []})
    suggestions = get_game_suggestions(query)
    return JsonResponse({'results': suggestions})