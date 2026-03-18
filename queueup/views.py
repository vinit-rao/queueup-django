import uuid
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from .igdb import fetch_game_data, get_game_suggestions

from .forms import CreatePost
from .models import Post, JoinRequest
from django.contrib.auth.decorators import login_required
from . import forms


def home(request):
    random_posts = Post.objects.all().order_by('?')[:4]
    return render(request, 'home.html', {'posts': random_posts})


def tutorial(request):
    return render(request, 'tutorial.html')


def about(request):
    return render(request, 'about.html')


def posts_list(request):
    query = request.GET.get('q')
    posts = Post.objects.all().order_by('-date')

    if query:
        terms = query.split()
        q_objects = Q()

        for term in terms:
            if term.startswith('#') and len(term) > 1:
                tag_word = term[1:]
                q_objects |= Q(tags__icontains=tag_word)
            else:
                q_objects |= Q(title__icontains=term) | Q(author__username__icontains=term)

        posts = posts.filter(q_objects).distinct()

    return render(request, 'posts/posts_list.html', {
        'posts': posts,
        'query': query
    })


def post_page(request, slug):
    post = get_object_or_404(Post, slug=slug)

    has_applied = False
    application_status = None

    if request.user.is_authenticated:
        application = JoinRequest.objects.filter(post=post, applicant=request.user).first()
        if application:
            has_applied = True
            application_status = application.status
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
        'has_applied': has_applied,
        'application_status': application_status
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


@login_required(login_url='/users/login/')
def my_posts_view(request):
    user_posts = Post.objects.filter(author=request.user).annotate(
        pending_count=Count('join_requests', filter=Q(join_requests__status='Pending'))
    ).order_by('-date')
    joined_posts = Post.objects.filter(
        join_requests__applicant=request.user,
        join_requests__status='Accepted'
    ).order_by('-date')
    return render(request, 'posts/my_posts.html', {
        'posts': user_posts,
        'joined_posts': joined_posts
    })


@login_required(login_url='/users/login/')
def manage_lobby(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user != post.author:
        return HttpResponseForbidden("You are not the host of this lobby.")
    applications = JoinRequest.objects.filter(post=post, status='Pending')

    return render(request, 'queueup/manage_lobby.html', {
        'post': post,
        'applications': applications
    })


@login_required(login_url='/users/login/')
def update_request(request, request_id, action):
    join_request = get_object_or_404(JoinRequest, id=request_id)
    if request.user != join_request.post.author:
        return HttpResponseForbidden("Not authorized.")
    if action == 'accept':
        join_request.status = 'Accepted'
    elif action == 'reject':
        join_request.status = 'Rejected'

    join_request.save()
    return JsonResponse({'success': True, 'action': action, 'request_id': request_id})


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