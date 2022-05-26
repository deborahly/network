import json
from multiprocessing.spawn import is_forking
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Follow, Like


def index(request):
    return render(request, "network/index.html")


def following(request):
    return render(request, "network/following.html")


def profile(request, username):
    profile_user = User.objects.get(username=username)
    if request.method == "POST":
        data = json.loads(request.body)
        active = data.get("active", "")
        # If now following: False -> True
        if active == "False":
            try:
                f = Follow.objects.get(follower=request.user, followed=profile_user)
            # If first time following, create new follow
            except:
                new_f = Follow.objects.create(follower=request.user, followed=profile_user)
                new_f.save()
                return JsonResponse({
                    "message": f"{request.user} is now following {profile_user}.",
                    "active": "True"
                }, status=200)
            # If not first time following, update follow
            f.active = True
            f.save()
            return JsonResponse({
                "message": f"{request.user} is now following {profile_user}.",
                "active": "True"
            }, status=201)
        # If now unfollowing: True -> False
        else:
            f = Follow.objects.get(follower=request.user, followed=profile_user)
            f.active = False
            f.save()
            return JsonResponse({
                "message": f"{request.user} is not following {profile_user}.",
                "active": "False"
            }, status=200)
    following = Follow.objects.filter(follower=profile_user, active=True)
    followers = Follow.objects.filter(followed=profile_user, active=True)  
    try:
        f = Follow.objects.get(follower=request.user, followed=profile_user, active='True')
    except:
        return render(request, "network/profile.html", {
            "username": username,
            "following": following,
            "followers": followers,
        })
    return render(request, "network/profile.html", {
        "username": username,
        "following": following,
        "followers": followers,
        "f": "True"
    })


def posts(request):
    # Get parameters
    page_number = request.GET.get("page", "")
    view = request.GET.get("view", "")
    username = request.GET.get("username", "")
    # Retrieve posts from database
    if view == "all":
        posts = Post.objects.all().order_by("-created_on")
    if view == "following":
        # Get people request user follows
        list_following = []
        follows = request.user.follows.filter(active=True)
        for follow in follows:
            followed = follow.followed
            list_following.append(followed)
        # Get their posts
        posts = []
        for following in list_following:
            following_posts = Post.objects.filter(poster=following)
            posts.extend(following_posts)
    if view == "profile":
        poster = User.objects.get(username=username)
        posts = Post.objects.filter(poster=poster)
    # Add paginator
    per_page = 2
    paginator = Paginator(posts, per_page)
    page_object = paginator.get_page(page_number)
    # Add likes information
    posts = []
    for post in page_object.object_list:
        if post.likes_received.filter(liked_by=request.user).exists():
            dict = post.serialize1()
            posts.append(dict)
        else:
            dict = post.serialize2()
            posts.append(dict)
    # Add poster information
    for post in posts:
        if post["poster"] == request.user.username:
            post.update({"user_is_author": True})
        else:
            post.update({"user_is_author": False})
    payload = {
        "page": {
            "current": page_object.number,
            "has_next": page_object.has_next(),
            "has_previous": page_object.has_previous()
        },
        "posts": posts
    }
    return JsonResponse(payload, safe=False)


def like(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post_id = data.get("post_id", "")
        # Check if post exists
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({}, status=400)
        # Check if user likes post
        try:
            l = Like.objects.get(post=post_id, liked_by=request.user)
            # In case user likes post, unlike it
            l.liked_by.remove(request.user)
            l.save()
            return JsonResponse({}, status=200)
        # If not, retrieve Like object and add user or create Like object with user 
        except Like.DoesNotExist:
            # Try to retrieve Like object and add user
            try:
                l = Like.objects.get(post=post_id)
                l.liked_by.add(request.user)
                l.save()   
            # Else create Like object with user
            except Like.DoesNotExist:
                l = Like.objects.create(post=post)
                l.liked_by.add(request.user)
                l.save()
                return JsonResponse({}, status=200)
            return JsonResponse({}, status=200)        


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


def save(request):
    # If method is not POST, return error message and status 400 (Bad Request)
    if request.method != "POST":
        return JsonResponse({
            "message": "POST request required."
            }, status=400)
    # Get request data
    data = json.loads(request.body)
    content = data.get("content", "")
    post_id = data.get("post_id", "")
    # Get poster
    poster = User.objects.get(username=request.user)
    # If post exists (post is being edited), update it
    try:
        post = Post.objects.get(id=post_id)
        post.content = content
        # Check if content is valid
        if post.is_valid_post() == True:
            post.edited = True
            post.save()
            return JsonResponse({}, status=200)
        else:
            return JsonResponse({
                "message": "Content cannot be empty nor contain more than 150 characters."
            }, status=400)
    # Is post does not exist, create it
    except:
        # Create post, without saving it yet
        post = Post(poster=poster, content=content)
        if post.is_valid_post() == True:
            post.save()
            return JsonResponse({}, status=200)
        else:
            return JsonResponse({
                "message": "Content cannot be empty nor contain more than 150 characters."
            }, status=400)