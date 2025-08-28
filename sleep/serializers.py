from rest_framework import serializers
from .models import SleepLog, SleepStage, SleepStageType, SleepSolfeggioRecommendation

class SleepStageSerializer(serializers.ModelSerializer):
    stage_name = serializers.CharField(source='stage_type.name', read_only=True)
    
    class Meta:
        model = SleepStage
        fields = ['id', 'stage_type', 'stage_name', 'duration_minutes']

class SleepSolfeggioSerializer(serializers.ModelSerializer):
    frequency_name = serializers.CharField(source='frequency.name', read_only=True)
    
    class Meta:
        model = SleepSolfeggioRecommendation
        fields = ['id', 'frequency', 'frequency_name', 'reason']

class SleepLogSerializer(serializers.ModelSerializer):
    stages = SleepStageSerializer(many=True, read_only=True)
    solfeggio_recommendations = SleepSolfeggioSerializer(many=True, read_only=True)
    
    class Meta:
        model = SleepLog
        fields = [
            'id', 'user', 'sleep_start', 'sleep_end', 'total_duration',
            'quality_score', 'mood_after', 'rituals', 'dream_notes',
            'date', 'stages', 'solfeggio_recommendations'
        ]
        read_only_fields = ['total_duration', 'user']
