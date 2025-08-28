from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class WorkoutSession(models.Model):
    WORKOUT_CHOICES = [
        ('yoga', 'Yoga'),
        ('cardio', 'Cardio'),
        ('strength', 'Strength Training'),
        ('pilates', 'Pilates'),
        ('stretching', 'Stretching'),
        ('meditation', 'Meditative Movement'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="workouts"
    )
    type = models.CharField(max_length=50, choices=WORKOUT_CHOICES)
    duration_minutes = models.PositiveIntegerField(default=0)
    energy_effect = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5,
        help_text="Energy effect rating (1-10)"
    )
    date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-created_at"]
        verbose_name = "Workout Session"
        verbose_name_plural = "Workout Sessions"

    def __str__(self):
        return f"{self.user.username} - {self.type} ({self.date})"
