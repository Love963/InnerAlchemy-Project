from rest_framework import serializers
from .models import Habit, HabitLog

class HabitLogSerializer(serializers.ModelSerializer):
    habit_name = serializers.CharField(source="habit.name", read_only=True)

    class Meta:
        model = HabitLog
        fields = ['id', 'habit', 'habit_name', 'date', 'status', 'notes']


class HabitSerializer(serializers.ModelSerializer):
    logs = HabitLogSerializer(many=True, read_only=True)
    current_streak = serializers.IntegerField(read_only=True)
    completion_rate = serializers.FloatField(read_only=True)

    class Meta:
        model = Habit
        fields = [
            'id', 'name', 'description', 'frequency', 'is_active',
            'created_at', 'current_streak', 'completion_rate', 'logs'
        ]
