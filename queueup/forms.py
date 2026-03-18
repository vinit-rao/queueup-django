from django import forms
from . import models

class CreatePost(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text="Enter up to 5 tags, separated by commas (max 12 chars each)"
    )

    class Meta:
        model = models.Post
        fields = ['title', 'body', 'game_name', 'tags']

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')

        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]

        if len(tag_list) > 5:
            raise forms.ValidationError("Maximum 5 tags allowed.")

        for tag in tag_list:
            if len(tag) > 12:
                raise forms.ValidationError(f"Tag '{tag}' is too long (max 12 characters).")

        return ",".join(tag_list)

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