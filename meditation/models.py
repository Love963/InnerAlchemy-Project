from django.db import models
from django.conf import settings
from django.utils import timezone
from solfeggio.models import SolfeggioFrequency
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
MOOD_CHOICES = [
    ("calm", "Calm"),
    ("relaxed", "Relaxed"),
    ("happy", "Happy"),
    ("grateful", "Grateful"),
    ("focused", "Focused"),
    ("energized", "Energized"),
    ("neutral", "Neutral"),
    ("thoughtful", "Thoughtful"),
    ("tired", "Tired"),
]

SPIRIT_LEVEL_CHOICES = [
    ("low", "Low - grounded, but not very connected"),
    ("balanced", "Balanced - stable and centered"),
    ("elevated", "Elevated - deeply connected, high energy"),
    ("transcendent", "Transcendent - unity, deep spiritual experience"),
]

class MeditationSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="meditations")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField()
    clarity_score = models.PositiveIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text = "Rate clarity"
    )

    duration_minutes = models.PositiveIntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(600)],
        help_text = "Duration in minutes"
    )

    focus_level = models.PositiveIntegerField(
    null=True, blank=True,
    validators=[MinValueValidator(1), MaxValueValidator(10)],
    help_text="Rate focus 1-10"
)

    mood_before = models.CharField(max_length=50, choices=MOOD_CHOICES, blank=True)
    mood_after = models.CharField(max_length=50, choices=MOOD_CHOICES, blank=True)

    spirit_level = models.CharField(max_length=20, choices=SPIRIT_LEVEL_CHOICES, default="balanced")

    solfeggio_frequency = models.ForeignKey(SolfeggioFrequency, null=True, blank=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-date"]
        verbose_name = "Meditation Session"
        verbose_name_plural = "Meditation Sessions"

    def __str__(self):
        return f"{self.title} - {self.user.username}"
