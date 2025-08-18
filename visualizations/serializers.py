from rest_framework import serializers
from .models import VisualizationAffirmation 

class VisualizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisualizationAffirmation
        fields = ['id', 'user', 'title', 'content', 'tags', 'solfeggio_frequency', 'date_created']
