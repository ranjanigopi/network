from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import User, Posts, Follows, Like
from .models import NewPost
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

POSTS_ORDER='-created'


def get_posts_in_page(request, posts):
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    return paginator.get_page(page)


def is_following(follower, followee):
    follow = Follows.objects.filter(follower=follower, followee=followee)
    return bool(follow)


def index(request):
    posts = Posts.objects.all().order_by(POSTS_ORDER)
    return render(request, "network/index.html", {
        "all_posts": get_posts_in_page(request, posts)
    })


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


def new_post(request):
    form = NewPost(request.POST or None)
    if form.is_valid():
        p = Posts(
            **form.cleaned_data,
            creator=request.user
        )
        p.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "network/new_post.html", {
        "form": form
    })


def profile(request, id):
    user_profile = User.objects.get(id=id)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "follow":
            f = Follows(follower=request.user, followee=user_profile)
            f.save()
        elif action == "unfollow":
            Follows.objects.filter(follower=request.user, followee=user_profile).delete()

    return render(request, "network/profile.html", {
        "all_posts": get_posts_in_page(request, user_profile.posts.all().order_by(POSTS_ORDER)),
        "profile": user_profile,
        "is_following": is_following(request.user, id)
    })


def following(request):
    follows = Follows.objects.filter(follower=request.user.id)
    all_posts = Posts.objects.none()
    for f in follows:
        all_posts = all_posts | Posts.objects.filter(creator=f.followee)
    return render(request, "network/following.html", {
        "all_posts": get_posts_in_page(request, all_posts.order_by(POSTS_ORDER))
    })


@csrf_exempt
@login_required
def edit_post(request, id):
    p = Posts.objects.get(id=id)
    if p.creator.id is not request.user.id:
        return HttpResponse(status=401)
    if request.method == "PUT":
        data = json.loads(request.body)
        content = data.get("content")
        p.content = content
        p.save()
        return HttpResponse(status=204)
    return HttpResponse(status=400)


@csrf_exempt
@login_required
def like(request, post_id):
    if request.method == "PUT":
        user_likes = json.loads(request.body).get("likes")

        if not user_likes:
            Like.objects.filter(liker=request.user, post=post_id).delete()
        else:
            l = Like(liker=request.user, post_id=post_id)
            l.save()
        return JsonResponse({
            "count": Posts.objects.get(id=post_id).likes.count()
        })
    return HttpResponse(status=400)
