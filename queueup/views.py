from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from . models import Post
from django.contrib.auth.decorators import login_required
from . import forms

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