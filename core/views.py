from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from sleep.models import SleepLog
from breathwork.models import BreathworkSession
from gratitude.models import GratitudeEntry
from soulnotes.models import SoulNote
from .serializers import DashboardSerializer, UserActivitySerializer
from .models import UserActivity
# Create your views here.


User = get_user_model()

class UserActivityListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = UserActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserActivity.objects.filter(user=self.request.user).order_by('-timestamp')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DashboardAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DashboardSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        sleep_logs = SleepLog.objects.filter(user=user)
        breathwork_sessions = BreathworkSession.objects.filter(user=user)
        gratitude_entries = GratitudeEntry.objects.filter(user=user)
        soulnotes = SoulNote.objects.filter(user=user)

        data = {
            'user': user,
            'sleep_logs': sleep_logs,
            'breathwork_sessions': breathwork_sessions,
            'gratitude_entries': gratitude_entries,
            'soulnotes': soulnotes,
        }
        serializer = self.serializer_class(data)
        return Response(serializer.data)
