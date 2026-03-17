from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomRegisterForm(UserCreationForm):
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user.profile.date_of_birth = self.cleaned_data.get('date_of_birth')
            user.profile.save()
        return user