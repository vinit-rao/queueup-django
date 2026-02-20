from django.contrib import admin
from django.urls import path, include
from gamehotspot import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('tutorial/', views.tutorial, name='tutorial'),
    path('about/', views.about, name='about'),
    path('posts/', include('gamehotspot.urls'))

]
