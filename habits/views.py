from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Habit, HabitLog
from .serializers import HabitSerializer, HabitLogSerializer
# Create your views here.
class HabitListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user, is_active=True)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
class HabitDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)
class HabitLogListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HabitLog.objects.filter(habit_user=self.request.user)
    def perform_create(self, serializer):
        habit = serializer.validated_data.get("habit")
        if habit.user != self.request.user:
            raise PermissionError("You cannot log habits for other users.")
        serializer.save()
    