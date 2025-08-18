from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings



# Create your models here.
class MeditationSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    mood_before = models.CharField(max_length=50, blank=True)
    mood_after = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
    