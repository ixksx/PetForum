from django.contrib import admin
from .models import Post, PostLike, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ["author", "content", "created_at"]
    can_delete = False

    def has_add_permission(self, request, obj):
        return False


class PostLikeInline(admin.TabularInline):
    model = PostLike
    extra = 0
    readonly_fields = ["user", "is_like", "created_at"]
    can_delete = False

    def has_add_permission(self, request, obj):
        return False


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "author",
        "content_preview",
        "created_at",
        "likes_count",
        "dislikes_count",
        "comments_count",
    ]
    list_filter = ["created_at", "author"]
    search_fields = ["content", "author__username"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [CommentInline, PostLikeInline]

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    content_preview.short_description = "Содержание"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "post_preview", "content_preview", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["content", "author__username"]
    readonly_fields = ["created_at"]

    def post_preview(self, obj):
        return (
            obj.post.content[:30] + "..."
            if len(obj.post.content) > 30
            else obj.post.content
        )

    post_preview.short_description = "Пост"

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    content_preview.short_description = "Комментарий"


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "post", "is_like", "created_at"]
    list_filter = ["is_like", "created_at"]
    search_fields = ["user__username"]
    readonly_fields = ["created_at"]

