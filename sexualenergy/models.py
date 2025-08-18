from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class SexualEnergySession(models.Model):
    TRANSFORMATION_CHOICES = [
        ('creativity', 'Creativity'),
        ('focus', 'Focus'),
        ('love', 'Love/Compassion'),
        ('healing', 'Healing'),
        ('manifestation', 'Manifestation'),
        ('spiritual', 'Spiritual Growth'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    intention = models.CharField(max_length=50, choices=TRANSFORMATION_CHOICES)
    practice_notes = models.TextField(blank=True, null=True)
    duration_minutes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.intention} ({self.created_at.date()})"


class SexualEnergyLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # fixed
    urges_felt = models.BooleanField(default=False)
    energy_level = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        default=5
    )
    redirect_activity = models.CharField(max_length=100, blank=True, null=True)  # e.g. "Breathwork", "Meditation"
    reflection = models.TextField(blank=True, null=True)
    logged_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - Energy:{self.energy_level}/10"
