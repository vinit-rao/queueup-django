from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def tutorial(request):
    return render(request, 'tutorial.html')