from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from . models import Post
from django.contrib.auth.decorators import login_required
from . import forms

def home(request):
    return render(request, 'home.html')

def tutorial(request):
    return render(request, 'tutorial.html')

def about(request):
    return render(request, 'about.html')

def posts_list(request):
    posts = Post.objects.all()
    return render(request, 'posts/posts_list.html', {'posts':posts})

def post_page(request, slug):
    post= Post.objects.get(slug=slug)
    return render(request, 'posts/post_page.html', {'post': post})

@login_required(login_url='/users/login')
def post_new(request):
    if request.method == 'POST':
        form = forms.CreatePost(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('posts:list')
    else:
        form = forms.CreatePost()
    return render(request, 'posts/post_new.html', {'form': form})


@login_required(login_url='/users/login/')
def lobby_view(request, lobby_name):
    post = get_object_or_404(Post, slug=lobby_name)
    messages = post.messages.all()[:50]
    return render(request, 'queueup/lobby.html', {
        'post': post,
        'lobby_name': lobby_name,
        'messages': messages
    })