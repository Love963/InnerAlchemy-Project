from rest_framework import serializers
from django.utils import timezone
from django.db.models import Count, Sum
from .models import Challenge, ChallengeMembership, ChallengeProgress


class ChallengeSerializer(serializers.ModelSerializer):
    created_by_name = serializers.ReadOnlyField(source="created_by.username")
    participant_count = serializers.IntegerField(read_only=True)
    is_owner = serializers.SerializerMethodField()
    is_participant = serializers.SerializerMethodField()
    is_active = serializers.ReadOnlyField()

    class Meta:
        model = Challenge
        fields = [
            "id",
            "title",
            "description",
            "visibility",
            "goal_type",
            "target_value",
            "unit",
            "start_date",
            "end_date",
            "created_by",
            "created_by_name",
            "participant_count",
            "is_owner",
            "is_participant",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "created_by", "participant_count", "is_owner", "is_participant", "is_active", "created_at"]

    def get_is_owner(self, obj):
        request = self.context.get("request")
        return bool(request and request.user.is_authenticated and obj.created_by_id == request.user.id)

    def get_is_participant(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return obj.memberships.filter(user=request.user, status="joined").exists()

    def to_representation(self, instance):
        # annotate participant count
        rep = super().to_representation(instance)
        rep["participant_count"] = instance.memberships.filter(status="joined").count()
        return rep

    def validate(self, data):
        start = data.get("start_date", getattr(self.instance, "start_date", None))
        end = data.get("end_date", getattr(self.instance, "end_date", None))
        if start and end and end < start:
            raise serializers.ValidationError({"end_date": "End date cannot be before start date."})
        return data

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class ChallengeProgressSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source="user.username")
    challenge_title = serializers.ReadOnlyField(source="challenge.title")

    class Meta:
        model = ChallengeProgress
        fields = [
            "id",
            "challenge",
            "challenge_title",
            "user",
            "user_name",
            "date",
            "value",
            "note",
            "created_at",
        ]
        read_only_fields = ["id", "user", "created_at"]

    def validate(self, data):
        # Ensure progress date is inside challenge window
        challenge = data.get("challenge") or self.instance.challenge
        date = data.get("date", timezone.localdate())
        if date < challenge.start_date or date > challenge.end_date:
            raise serializers.ValidationError({"date": "Progress date must be within the challenge window."})
        return data

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
