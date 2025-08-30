from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.
User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Optional links
    habit = models.ForeignKey(
        "habits.Habit",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_posts"
    )
    challenge = models.ForeignKey(
        "challenges.Challenge",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_posts"
    )

    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at:%Y-%m-%d}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.id}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "post")  # Prevent multiple likes from same user

    def __str__(self):
        return f"{self.user.username} liked Post {self.post.id}"
