from rest_framework import serializers
from .models import ColdShowerLog


class ColdShowerLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColdShowerLog
        fields = ['id', 'user', 'mood_before', 'mood_after', 'resistance_level', 'notes', 'date']
        read_only_fields = ['id', 'user', 'date']