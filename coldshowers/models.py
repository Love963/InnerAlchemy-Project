from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.
class ColdShowerLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mood_before = models.CharField(max_length=50)
    mood_after = models.CharField(max_length=50)
    resistance_level = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)], default=5)
    notes = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.date} - Resistance:(self.resistance_level)"
    