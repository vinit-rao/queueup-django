from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . models import Post

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