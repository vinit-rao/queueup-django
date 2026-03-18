from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CustomRegisterForm(UserCreationForm):
    date_of_birth = forms.DateField(required=False)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields
    def save(self, commit=True):
        user = super().save(commit=commit)
        return user

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages['invalid_login'] = "Incorrect username or password."