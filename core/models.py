from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
# Create your models here.

User = get_user_model()
USER = settings.AUTH_USER_MODEL

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    app_name = models.CharField(max_length=100)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.app_name} - {self.action}"




PERIOD_CHOICES = [
    ("weekly", "Weekly"),
    ("monthly", "Monthly"),
]

class SummaryReport(models.Model):
    """
    Persisted summary report for a user for a given period window.
    `start_date` is inclusive; `end_date` is inclusive.
    `metrics` stores computed normalized scores and optionally breakdowns.
    """
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="summary_reports")
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()

    # JSON payload that holds all computed metric values and breakdowns
    # Example:
    # {
    #   "energy": {"score": 78.5, "sources": {"workouts": 80, "nutrition": 75}},
    #   "clarity": {"score": 60, "sources": {"meditation": 60, "sleep": 55}},
    #   ...
    # }
    metrics = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("user", "period", "start_date", "end_date")

    def __str__(self):
        return f"{self.user} {self.period} {self.start_date}→{self.end_date}"
