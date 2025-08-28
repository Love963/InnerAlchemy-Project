from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Create your models here.
class GratitudeEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    tags = models.CharField(max_length=200, blank=True, null=True)
    gratitude_score = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    solfeggio_frequency = models.ForeignKey(
        'solfeggio.SolfeggioFrequency',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    date = models.DateField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)   
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.date} - Score:{self.gratitude_score}"

