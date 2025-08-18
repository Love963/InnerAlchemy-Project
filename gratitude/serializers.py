from rest_framework import serializers
from .models import GratitudeEntry

class GratitudeEntrySerializer(serializers.ModelSerializer):
    class Meta:
        models = GratitudeEntry
        fields = ['id', 'user', 'content', 'tags', 'gratitude_score', 'solfeggio_frequency', 'date']
        read_only_fields = ['id', 'user', 'date']
        
 