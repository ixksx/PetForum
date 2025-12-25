from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from .forms import RegisterForm, LoginForm
from .models import User, UserActivity
from posts.models import Post


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            user.update_last_seen()

            refresh = RefreshToken.for_user(user)

            request.session["access_token"] = str(refresh.access_token)
            request.session["refresh_token"] = str(refresh)

            next_url = request.GET.get("next", "home")
            return redirect(next_url)
    else:
        form = LoginForm()

    next_url = request.GET.get("next", "")
    return render(request, "login.html", {"form": form, "next": next_url})


def logout_view(request):
    logout(request)
    return redirect("home")


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by("-created_at")

    if request.user.is_authenticated and request.user != user:
        UserActivity.objects.create(
            user=user,
            activity_type="profile_view",
            details=f"Просмотр профиля пользователем {request.user.username}",
        )

    context = {
        "profile_user": user,
        "posts": posts,
    }

    return render(request, "profile.html", context)


@csrf_exempt
@login_required
def update_last_seen(request):
    if request.method == "POST":
        request.user.update_last_seen()
        return JsonResponse(
            {"status": "success", "last_seen": request.user.last_seen.isoformat()}
        )
    return JsonResponse({"status": "error"}, status=400)

