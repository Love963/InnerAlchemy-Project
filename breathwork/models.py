from django.db import models
from django.contrib.auth import get_user_model
from solfeggio.models import SolfeggioFrequency  # Optional link
# Create your models here.
User = get_user_model()

class BreathworkSession(models.Model):
    TECHNIQUES = [
        ('Bhastrika', 'Bhastrika'),
        ('Kapalabhati', 'Kapalabhati'),
        ('Wim Hof', 'Wim Hof'),
        ('Mula Bandha', 'Uddiyana Bandha'),
        ('Microcosmic Orbit', 'Microcosmic Orbit'),
        ('Other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='breathwork_sessions')
    technique = models.CharField(max_length=100, choices=TECHNIQUES)
    duration = models.PositiveBigIntegerField(help_text='Duration in minutes')
    energy_level = models.PositiveBigIntegerField(help_text='Rate energy 1-10')
    experience_notes = models.TextField(blank=True, null=True)
    solfeggio_frequency = models.ForeignKey(
        SolfeggioFrequency, null=True, blank=True, on_delete=models.SET_NULL
    )
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
    def __str__(self):
        return f"{self.user.username} - {self.technique} on {self.date}"
    