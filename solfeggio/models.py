from django.db import models

# Create your models here.
class SolfeggioFrequency(models.Model):
    frequency_hz = models.PositiveBigIntegerField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.frequency_hz} Hz)"