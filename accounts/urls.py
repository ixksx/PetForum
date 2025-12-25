from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("users/<str:username>/", views.profile_view, name="profile"),
    path("api/update-last-seen/", views.update_last_seen, name="update_last_seen"),
]