from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    slug = models.SlugField(max_length=100, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    game_name = models.TextField(max_length=200, blank=True, null=True)
    banner_url = models.URLField(max_length=500, blank=True, null=True)
    cover_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title


class JoinRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Joined', 'Joined'),
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='join_requests')
    # Links the request to the user applying
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    # The text field for their application message
    message = models.TextField(max_length=500)
    # The current status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.username} applying to {self.post.title}"

class Message(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.user.username} on {self.post.title}: {self.content[:20]}"