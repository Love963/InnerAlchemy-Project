from rest_framework import serializers
from .models import SexualEnergySession, SexualEnergyLog

class SexualEnergySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SexualEnergySession
        fields = ['id', 'user', 'intention', 'practice_notes', 'duration_minutes', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

class SexualEnergyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SexualEnergyLog
        fields = ['id', 'user', 'urges_felt', 'energy_level', 'redirect_activity', 'reflection', 'logged_at']
        read_only_fields = ['id', 'user', 'logged_at']
