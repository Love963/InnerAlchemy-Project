from django.shortcuts import render
from rest_framework import generics, permissions
# Create your views here.
from .models import GratitudeEntry
from .serializers import GratitudeEntrySerializer

class GratitudeListCreateAPI(generics.ListCreateAPIView):
    serializer_class = GratitudeEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users see only their own gratitude entries
        return GratitudeEntry.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
class GratitudeDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GratitudeEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only access their own entries
        return GratitudeEntry.objects.filter(user=self.request.user)
    
    