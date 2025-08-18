from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.
class VisualizationAffirmation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.CharField(max_length=200, blank=True, null=True)
    solfeggio_frequency = models.ForeignKey(
        'solfeggio.SolfeggioFrequency',   # link with solfeggio app
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} ({self.user.username})"
