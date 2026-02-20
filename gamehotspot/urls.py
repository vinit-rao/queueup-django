from django.urls import path
from gamehotspot import views

urlpatterns = [
    path('', views.posts_list),
]