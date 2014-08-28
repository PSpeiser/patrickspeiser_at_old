from django.shortcuts import render
from models import Post
import datetime
from json_functions import json_response
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "blog/home.html", {'posts': Post.objects.order_by('date').reverse()})


@login_required
def editor(request):
    return render(request, "blog/editor.html")


def markdown_js(request):
    return render(request, "blog/markdown.js")


@login_required
def add_blog_post(request):
    if request.method == "POST":
        post = Post()
        post.title = request.POST.get('title')
        post.text = request.POST.get('text')
        if not post.title or not post.text:
            return HttpResponse("400 Bad Request You need to specify a title and message")
        post.date = datetime.datetime.now()
        post.save()
        return json_response(request, 'Success')
    else:
        return HttpResponse("405 Method Not Allowed")
