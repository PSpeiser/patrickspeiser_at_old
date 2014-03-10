from django.views.decorators.cache import cache_page
from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def certificates(request):
    return render(request,'certificates.html')