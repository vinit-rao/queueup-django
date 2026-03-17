from django import forms
from . import models

class CreatePost(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title', 'body', 'game_name']

class JoinRequestForm(forms.ModelForm):
    class Meta:
        model = models.JoinRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Tell the host your rank, role, or why you want to join...'
            })
        }