import json
import datetime
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from network.models import *


def index(request):
    return render(request, "network/index.html")

def profilepage(request, id):
    return render(request, "network/profile.html")

def following(request, id):
    return render(request, "network/following.html")

@csrf_exempt
@login_required
def compose(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)

    body = data.get("body", "")

    post = Post(
        user= request.user,
        body=body,
        )
    post.save()
    return JsonResponse({"message": "Post made successfully."}, status=201)


def posts(request, page):
    posts = Post.objects.all()
    list = [post.serialize(request.user.username) for post in posts.order_by("-timestamp").all()]
    pages = Paginator(list, 10).page(page)
    return JsonResponse({
        "posts": pages.object_list,
        "hasnextpage": pages.has_next(),
        "haspreviouspage": pages.has_previous()
        }, safe=False)

def followpost(request, id, page):
    me = User.objects.filter(pk=id).all()[0]
    list = [post.serialize(me.username) for post in Post.objects.filter(user__in=map(lambda profile: profile.user, me.following.all())).order_by("-timestamp").all()]
    pages = Paginator(list, 10).page(page)

    return JsonResponse({
        "posts": pages.object_list,
        "hasnextpage": pages.has_next(),
        "haspreviouspage": pages.has_previous()
    }, safe=False)

def profile(request, id, page):
    user = User.objects.filter(pk=id).all()[0]
    try: 
        user.profile.followers
    except ObjectDoesNotExist:
        profile = Profile(
            user = user,
        )
        profile.save()
    list = [post.serialize(user.username) for post in user.posts.order_by("-timestamp").all()]
    pages = Paginator(list, 10).page(page)

    return JsonResponse({
        "username": user.username,
        "followingCount": user.following.count(),
        "followerCount" : user.profile.followers.count(),
        "posts": pages.object_list,
        "hasnextpage": pages.has_next(),
        "haspreviouspage": pages.has_previous(),
        "isFollowing": user.profile.followers.filter(pk=request.user.pk).count() == 1,
        "is_me": request.user.pk == id,
        "userid": id
    }, safe=False)


@csrf_exempt
@login_required
def edit(request, post_id):


    try:
        post = Post.objects.get(user=request.user, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)


    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("body") is not None:
            post.body = data["body"]
        post.save()
        return HttpResponse(status=204)


    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)


@csrf_exempt
@login_required
def follow(request, id):


    try:
        user = User.objects.get(pk=id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)


    if request.method == "PUT":
        if request.user in user.profile.followers.all():
            user.profile.followers.remove(request.user)
            user.profile.save()
        else:
            user.profile.followers.add(request.user)
            user.profile.save()
        return HttpResponse(status=204)


    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

@csrf_exempt
@login_required
def like(request, post_id):


    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)


    if request.method == "PUT":
        if request.user in post.likers.all():
            post.likers.remove(request.user)
            post.save()
        else:
            post.likers.add(request.user)
            post.save()
        return HttpResponse(status=204)


    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)


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
