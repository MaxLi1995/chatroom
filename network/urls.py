
from django.urls import path

from network import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profilepage/<int:id>", views.profilepage, name="profilepage"),
    path("following/<int:id>", views.following, name="following"),


# API Routes
    path("compose", views.compose, name="compose"),
    path("posts/<int:page>", views.posts, name="posts"),
    path("like/<int:post_id>", views.like, name="like"),
    path("follow/<int:id>", views.follow, name="follow"),
    path("profile/<int:id>/<int:page>", views.profile, name="profile"),
    path("followpost/<int:id>/<int:page>", views.followpost, name="followpost"),
    path("edit/<int:post_id>", views.edit, name="edit")
]