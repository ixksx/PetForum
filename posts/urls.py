from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("create-posts/", views.create_post_view, name="create_post"),
    path("posts/<int:pk>/", views.post_detail_view, name="post_detail"),
    path("posts/<int:pk>/like/", views.like_post_view, name="like_post"),
    path("posts/<int:pk>/delete/", views.delete_post_view, name="delete_post"),
]