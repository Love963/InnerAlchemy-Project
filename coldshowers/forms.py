from django import forms
from .models import ColdShowerLog

class ColdShowerLogForm(forms.ModelForm):
    class Meta:
        model = ColdShowerLog
        fields = ['mood_before', 'mood_after', 'resistance_level', 'notes', 'date']
