from rest_framework import serializers
from .models import GratitudeEntry

class GratitudeEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = GratitudeEntry  
        fields = [
            'id',
            'user',
            'content',
            'tags',
            'gratitude_score',
            'solfeggio_frequency',
            'date',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'date', 'created_at', 'updated_at']
