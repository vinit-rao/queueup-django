from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .forms import CustomRegisterForm
from .models import Profile


def register_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            gender = request.POST.get('gender')
            dob = request.POST.get('date_of_birth')
            profile = Profile.objects.get(user=user)
            profile.gender = gender
            if dob:
                profile.date_of_birth = dob
            profile.save()

            login(request, user)
            return redirect("posts:list")
        else:
            print(form.errors)
            return render(request, "users/register.html", {"form": form}, status=400)
    else:
        form = CustomRegisterForm()
    return render(request, "users/register.html", {"form": form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            return redirect("posts:list")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect("posts:list")