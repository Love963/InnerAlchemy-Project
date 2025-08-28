from django import forms
from .models import SoulNote

class SoulNoteForm(forms.ModelForm):
    class Meta:
        model = SoulNote
        fields = ['title', 'content', 'tags', 'mood', 'solfeggio_frequency']