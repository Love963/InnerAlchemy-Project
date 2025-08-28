from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

# Create your models here.
User = get_user_model()


class Habit(models.Model):
    FREQUENCY_CHOICES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default="daily")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    # Computed Properties
    @property
    def current_streak(self):
        logs = self.logs.filter(status="done").order_by("-date")
        streak = 0
        today = timezone.now().date()

        for log in logs:
            if log.date == today - timedelta(days=streak):
                streak += 1
            else:
                break
        return streak

    @property
    def completion_rate(self):
        total_logs = self.logs.count()
        done_logs = self.logs.filter(status="done").count()
        return round((done_logs / total_logs) * 100, 1) if total_logs > 0 else 0

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class HabitLog(models.Model):
    STATUS_CHOICES = [
        ("done", "Done"),
        ("skipped", "Skipped"),
        ("missed", "Missed"),
    ]

    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="logs")
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="done")
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("habit", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.habit.name} - {self.date} ({self.status})"


