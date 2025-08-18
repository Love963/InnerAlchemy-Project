from django.db import models
from django.conf import settings
from django.utils import timezone

class GratitudeEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    tags = models.CharField(max_length=200, blank=True, null=True)
    gratitude_score = models.PositiveIntegerField(default=0)
    solfeggio_frequency = models.ForeignKey(
        'solfeggio.SolfeggioFrequency',  # link to Solfeggio
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.date} - Score:{self.gratitude_score}"
