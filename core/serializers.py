from rest_framework import serializers
from users.serializers import UserSerializer
from sleep.serializers import SleepLogSerializer
from breathwork.serializers import BreathworkSessionSerializer
from gratitude.serializers import GratitudeEntrySerializer
from soulnotes.serializers import SoulNoteSerializer
from core.models import UserActivity
from .models import SummaryReport

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



class SummaryReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummaryReport
        fields = [
            "id",
            "user",
            "period",
            "start_date",
            "end_date",
            "metrics",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

class SummaryComputeSerializer(serializers.Serializer):
    """
    Input shape for on-demand compute:
      - period: 'weekly' or 'monthly'
      - start_date (optional): 'YYYY-MM-DD' (if omitted, compute last period ending today)
      - persist: boolean (optional) whether to save the computed summary
    """
    period = serializers.ChoiceField(choices=["weekly", "monthly"], required=True)
    start_date = serializers.DateField(required=False, allow_null=True)
    persist = serializers.BooleanField(default=False)
