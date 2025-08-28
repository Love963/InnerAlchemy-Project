from django import forms
from .models import MeditationSession

class MeditationSessionForm(forms.ModelForm):
    class Meta:
        model = MeditationSession
        fields = [
            'title', 'description', 'duration_minutes',
            'clarity_score', 'mood_before', 'mood_after',
            'spirit_level', 'solfeggio_frequency'
        ]
