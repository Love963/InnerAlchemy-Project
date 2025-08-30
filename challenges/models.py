from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.

User = get_user_model()

class Challenge(models.Model):
    VISIBILITY_CHOICES = [
        ("public", "Public"),
        ("private", "Private"),
    ]

    # define what is being measured
    GOAL_TYPE_CHOICES = [
        ("count", "Count-based (e.g., sessions, reps)"),
        ("duration", "Time-based (e.g., minutes per day)"),
        ("streak", "Streak-based (do it every day)"),
        ("custom", "Custom / subjective"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default="public")

    goal_type = models.CharField(max_length=20, choices=GOAL_TYPE_CHOICES, default="streak")
    target_value = models.FloatField(
        null=True, blank=True,
        help_text="Optional numeric target (e.g., 20 minutes/day or 10 sessions)."
    )
    unit = models.CharField(
        max_length=20, blank=True,
        help_text="Optional unit like 'min', 'sessions', 'km'."
    )

    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="challenges_created")

    participants = models.ManyToManyField(
        User,
        through="ChallengeMembership",
        related_name="challenges_joined",
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["visibility", "start_date", "end_date"]),
            models.Index(fields=["created_by"]),
        ]

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date.")

    @property
    def is_active(self):
        today = timezone.localdate()
        return self.start_date <= today <= self.end_date

    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days + 1

    def __str__(self):
        return f"{self.title} ({self.start_date} → {self.end_date})"


class ChallengeMembership(models.Model):
    STATUS_CHOICES = [
        ("joined", "Joined"),
        ("left", "Left"),
    ]

    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="challenge_memberships")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="joined")
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("challenge", "user")
        indexes = [
            models.Index(fields=["challenge", "user"]),
        ]

    def __str__(self):
        return f"{self.user} ↔ {self.challenge} ({self.status})"


class ChallengeProgress(models.Model):
    # A user's progress entry for a given challenge and date.
    # Enforce a single entry per (user, challenge, date).
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="progress_entries")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="challenge_progress")
    date = models.DateField(default=timezone.localdate)
    value = models.FloatField(
        null=True, blank=True,
        help_text="Numeric progress (e.g., minutes, reps). Optional for streak/custom."
    )
    note = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("challenge", "user", "date")
        ordering = ["-date", "-created_at"]
        indexes = [
            models.Index(fields=["challenge", "user", "date"]),
        ]

    def __str__(self):
        return f"{self.user} · {self.challenge.title} · {self.date} · {self.value or '-'}"
