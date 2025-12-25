from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserActivity


class UserActivityInline(admin.TabularInline):
    model = UserActivity
    extra = 0
    readonly_fields = ["activity_type", "details", "created_at"]
    can_delete = False

    def has_add_permission(self, request, obj):
        return False


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = [
        "username",
        "email",
        "is_staff",
        "is_online",
        "last_seen",
        "posts_count",
    ]
    list_filter = ["is_staff", "is_superuser", "is_active"]
    readonly_fields = ["last_seen", "posts_count"]
    inlines = [UserActivityInline]

    fieldsets = UserAdmin.fieldsets + (
        ("Дополнительная информация", {"fields": ("avatar", "last_seen")}),
    )


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ["user", "activity_type", "created_at"]
    list_filter = ["activity_type", "created_at"]
    search_fields = ["user__username", "details"]
    readonly_fields = ["user", "activity_type", "details", "created_at"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

