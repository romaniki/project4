
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add-post", views.add_post_form, name="form"),
    
    path("profile/<str:username>", views.profile, name="profile"),
    path("following/<str:username>", views.following, name="following"),

    path("post/<int:post_id>", views.post, name="post"),
    path("post-like/<int:post_id>", views.post_like, name="like"),
]
