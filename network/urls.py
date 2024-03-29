
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("save", views.save, name="save"),
    path("posts/", views.posts, name="posts"),
    path("following", views.following, name="following"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("like", views.like, name="like"),
    path("delete", views.delete, name="delete"),
]
