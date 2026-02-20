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
    return render(request, 'posts/posts_list.html', {'post':posts})