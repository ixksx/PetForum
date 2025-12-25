from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    last_seen = models.DateTimeField(default=timezone.now)

    @property
    def is_online(self):
        return (timezone.now() - self.last_seen).seconds < 300

    @property
    def posts_count(self):
        return self.posts.count()

    def update_last_seen(self):
        self.last_seen = timezone.now()
        self.save(update_fields=["last_seen"])

    def get_last_seen_display(self):
        time_since = timezone.now() - self.last_seen
        minutes = int(time_since.total_seconds() / 60)
        hours = int(minutes / 60)
        days = int(hours / 24)

        if minutes < 1:
            return "только что"
        elif minutes < 60:
            return f"{minutes} минут назад"
        elif hours < 24:
            return f"{hours} часов назад"
        else:
            return f"{days} дней назад"


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activities")
    activity_type = models.CharField(max_length=50)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

