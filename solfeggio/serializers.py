from rest_framework import serializers
from .models import SolfeggioFrequency

class SolfeggioFrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = SolfeggioFrequency
        fields = ['id', 'frequency_hz', 'name', 'description']
