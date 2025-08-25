from rest_framework import serializers
from users.serializers import UserSerializer
from sleep.serializers import SleepLogSerializer
from breathwork.serializers import BreathworkSessionSerializer
from gratitude.serializers import GratitudeEntrySerializer
from soulnotes.serializers import SoulNoteSerializer
from core.models import UserActivity

class UserActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserActivity
        fields = ['id', 'user', 'app_name', 'action', 'timestamp']

class DashboardSerializer(serializers.Serializer):
    user = UserSerializer()
    sleep_logs = SleepLogSerializer(many=True)
    breathwork_sessions = BreathworkSessionSerializer(many=True)
    gratitude_entries = GratitudeEntrySerializer(many=True)
    soulnotes = SoulNoteSerializer(many=True)
