from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.http import JsonResponse
from .forms import CustomRegisterForm, CustomLoginForm
from .models import Profile


def register_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
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
            if is_ajax:
                return JsonResponse({"success": True})
            return redirect("posts:list")
        else:
            if is_ajax:
                return JsonResponse({"errors": form.errors}, status=400)

            print(form.errors)
            return render(request, "users/register.html", {"form": form}, status=400)
    else:
        form = CustomRegisterForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        if form.is_valid():
            login(request, form.get_user())
            if is_ajax:
                return JsonResponse({"success": True})
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            return redirect("posts:list")
        else:
            if is_ajax:
                return JsonResponse({"errors": form.errors}, status=400)
            return render(request, "users/login.html", {"form": form})
    else:
        form = CustomLoginForm()

    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect("posts:list")