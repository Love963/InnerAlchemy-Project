from django.shortcuts import render
from rest_framework import generics, permissions
from .models import BreathworkSession
from .serializers import BreathworkSessionSerializer
# Create your views here.
class BreathworkSessionListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BreathworkSessionSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return BreathworkSession.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
class BreathworkSessionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BreathworkSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BreathworkSession.objects.filter(user=self.request.user)
    
    
    