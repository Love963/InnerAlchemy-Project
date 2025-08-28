from rest_framework import serializers
from .models import MeditationSession


class MeditationSessionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    mood_shift = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()

    class Meta:
        model = MeditationSession
        fields = [
            'id',
            'user',
            'title',
            'description',
            'duration_minutes',
            'clarity_score',
            'mood_before',
            'mood_after',
            'mood_shift',          
            'spirit_level',
            'solfeggio_frequency',
            'date',
            'summary',              
        ]

    def get_mood_shift(self, obj):
        # Show how the mood changed during meditation.
        if obj.mood_before and obj.mood_after:
            return f"{obj.mood_before} → {obj.mood_after}"
        return None

    def get_summary(self, obj):
        return (
            f"{obj.title} ({obj.duration_minutes} min) "
            f"| Spirit: {obj.spirit_level} "
            f"| Clarity: {obj.clarity_score or 'N/A'}"
        )
