from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from solfeggio.models import SolfeggioFrequency

# Create your models here.

User = get_user_model()

class Chakra(models.Model):
    # Master data for the 7 chakras (no user link)
    CODE_CHOICES = [
        ('root', '(Root (Muladhara))'),
        ('sacral', 'Sacral (Svadhisthana)'),
        ('solar_plexus', 'Solar Plexus (Manipura)'),
        ('heart', 'Heart (Anahata)'),
        ('throat', 'Throat (Vishuddha)'),
        ('third_eye', 'Third Eye (Ajna)'),
        ('crown', 'Crown (Sahasrara)'),
    ]
    code = models.CharField(max_length=20, choices=CODE_CHOICES, unique=True)
    name = models.CharField(max_length=60)                # e.g. "Heart"
    sanskrit_name = models.CharField(max_length=60)       # e.g. "Anahata"
    color = models.CharField(max_length=30, blank=True)   # e.g. "Green"
    element = models.CharField(max_length=30, blank=True) # e.g. "Air"
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name
class ChakraLog(models.Model):
    # Pre-user chakra tracking, with optional solfeggio frequency reference
    STATE_CHOICES = [
        ('balanced', 'Balanced'),
        ('open', 'Open'),
        ('blocked', 'Blocked'),
        ('underactive', 'Underactive'),
        ('overactive', 'Overactive'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chakra_logs')
    chakra = models.ForeignKey(Chakra, on_delete=models.PROTECT, related_name='logs')
    state = models.CharField(max_length=20, choices=STATE_CHOICES)
    intensity = models.PositiveIntegerField(null=True, blank=True, help_text='1-10 (optional)')
    notes = models.TextField(blank=True)
    solfeggio_frequency = models.ForeignKey(
        SolfeggioFrequency, null=True, blank=True, on_delete=models.SET_NULL, related_name='chakra_logs'
    )
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['chakra']),
        ]
    def __str__(self):
        return f'{self.user} . {self.chakra.name} . {self.state} . {self.date}'
        
        
    
