from rest_framework import serializers
from .models import BreathworkSession


class BreathworkSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreathworkSession
        fields = [
            'id', 'user', 'technique', 'duration', 'energy_level',
            'experience_notes', 'solfeggio_frequency', 'date'
        ]
        read_only_fields = ['id', 'user', 'date']
        