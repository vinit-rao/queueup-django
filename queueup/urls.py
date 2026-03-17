from django.urls import path
from queueup import views

app_name = 'posts'

urlpatterns = [
    path('', views.posts_list, name='list'),
    path('new-post/', views.post_new, name='new-post'),
    path('<slug:slug>', views.post_page, name='page'),
    path('chat/<slug:lobby_name>/', views.lobby_view, name='lobby'),
    path('api/games/search/', views.api_search_games, name='api-game-search'),
    path('my-posts/', views.my_posts_view, name='my-posts'),
]