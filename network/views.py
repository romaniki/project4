import json
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.views.decorators.csrf import requires_csrf_token, ensure_csrf_cookie
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator


from .forms import PostForm
from .models import User, Post, UserFollowing


def index(request):
    posts = Post.objects.all()
    posts = posts.order_by("-timestamp").all()
    paginator = Paginator(posts, 10) 
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # return JsonResponse({"meta":page_number,"data":[post.serialize() for post in page_obj]})
    return render(request, "network/index.html", {'page_obj': page_obj})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def add_post_form(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():

            post = form.save(commit=False)
            post.author = request.user
            post.save()
            if request.is_ajax():
                return JsonResponse(post.serialize(), status=201)
        
        if form.errors:
            if request.is_ajax():
                return JsonResponse(form.errors, status=400)

    return HttpResponseRedirect(reverse("index"))

def post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "GET":
        return JsonResponse(post.serialize(), status=200)
    
    elif request.method == "PUT":
        
        data = json.loads(request.body)
        post.content = data["content"]
        post.save()
        return HttpResponse(status=204)

@login_required
def post_like(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            post.save()
            return JsonResponse(post.serialize(), status=201)
        else:
            post.likes.add(request.user)
            post.save()
            return JsonResponse(post.serialize(), status=201)

def profile(request, username):
    user = User.objects.get(username=username)
    profile, created = UserFollowing.objects.get_or_create(user=user)
    followers = profile.following_user
    following = UserFollowing.objects.filter(following_user=user)
    
    is_followed = request.user in followers.all()
    if request.method == "POST" and request.user != user:
        if request.user in profile.following_user.all():
            profile.following_user.remove(request.user)
            profile.save()
        else:
            profile.following_user.add(request.user)
            profile.save()
            
        return HttpResponse(status=201)
        
    
    posts = Post.objects.filter(author=user)
    posts = posts.order_by("-timestamp").all()
    
    paginator = Paginator(posts, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'username': username,
        'followers': followers,
        'following': following,
        'target': user,
        'is_followed': is_followed,
    }
    return render(request, "network/profile.html", context)

@login_required
def following(request, username):
    user = User.objects.get(username=username)
    following = UserFollowing.objects.filter(following_user=user)

    following_set = [user.user for user in following]
    posts = Post.objects.filter(author__in=following_set)
    posts = posts.order_by("-timestamp").all()
    
    paginator = Paginator(posts, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, "network/following.html", context)
