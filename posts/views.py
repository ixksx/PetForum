import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Post, PostLike, Comment
from .forms import PostForm, CommentForm
from accounts.models import UserActivity


def home_view(request):
    posts = Post.objects.all().prefetch_related("likes", "comments")
    return render(request, "home.html", {"posts": posts})


@login_required
def create_post_view(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # Запись активности
            UserActivity.objects.create(
                user=request.user,
                activity_type="post_created",
                details=f"Создан пост: {post.content[:50]}...",
            )

            return redirect("home")
    else:
        form = PostForm()
    return render(request, "create_post.html", {"form": form})


def post_detail_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    user_reaction = None
    if request.user.is_authenticated:
        try:
            user_reaction = post.likes.get(user=request.user)
        except PostLike.DoesNotExist:
            pass

    if request.method == "POST" and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("post_detail", pk=pk)
    else:
        form = CommentForm()

    return render(
        request,
        "post_detail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
            "user_reaction": user_reaction,
        },
    )


@csrf_exempt
@login_required
def like_post_view(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)

        try:
            data = json.loads(request.body)
            is_like = data.get("is_like")
        except:
            return JsonResponse(
                {"status": "error", "message": "Invalid data"}, status=400
            )

        if isinstance(is_like, str):
            is_like = is_like.lower() == "true"

        PostLike.objects.filter(user=request.user, post=post).delete()

        PostLike.objects.create(user=request.user, post=post, is_like=is_like)

        post.refresh_from_db()

        return JsonResponse(
            {
                "status": "success",
                "likes_count": post.likes_count,
                "dislikes_count": post.dislikes_count,
            }
        )

    return JsonResponse({"status": "error"}, status=400)


@csrf_exempt
@login_required
def delete_post_view(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        if post.author == request.user or request.user.is_staff:
            post.delete()
            return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=403)

