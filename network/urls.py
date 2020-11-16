
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("like/<int:post_id>", views.like, name="like"),
    path("new", views.new_post, name="new"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("profile/<str:edit>", views.edit, name="edit"),
    path("following", views.following, name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
