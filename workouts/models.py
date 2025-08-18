from django.db import models
from django.conf import settings
# Create your models here.
from django.utils import timezone

class WorkoutSession(models.Model):
    WORKOUT_CHOICES = [
        ('yoga', 'Yoga'),
        ('cardio', 'Cardio'),
        ('strength', 'Strength Training'),
        ('pilates', 'Pilate'),
        ('stretching', 'Stretching'),
        ('meditation', 'Meditative Movement'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=WORKOUT_CHOICES)
    duration_minutes = models.PositiveIntegerField(default=0)
    energy_effect = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        default=5
    )
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.type} ({self.date})"
    