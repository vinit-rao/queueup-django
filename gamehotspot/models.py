from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    slug = models.SlugField(max_length=100, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(default='fm5.jpg', blank=True)

    def __str__(self):
        return self.title