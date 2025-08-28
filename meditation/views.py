from django.shortcuts import render
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import MeditationSession
from .serializers import MeditationSessionSerializer

# Create your views here.
#  List + Create API
class MeditationSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = MeditationSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['mood_before', 'mood_after', 'spirit_level', 'solfeggio_frequency']

    def get_queryset(self):
        # Only show sessions of the logged-in user
        return MeditationSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Auto-assign the user
        serializer.save(user=self.request.user)


# Retrieve + Update + Delete API
class MeditationSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MeditationSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # User can only access their own sessions
        return MeditationSession.objects.filter(user=self.request.user)
