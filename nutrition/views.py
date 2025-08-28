from django.shortcuts import render
from rest_framework import generics, permissions
from .models import NutritionLog
from .serializers import NutritionLogSerializer

# Create your views here.
# List & Create Nutrition Logs
class NutritionLogListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = NutritionLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return logs belonging to the authenticated user
        return NutritionLog.objects.filter(user=self.request.user).order_by("-date")

    def perform_create(self, serializer):
        # Automatically associate the log with the logged-in user
        serializer.save(user=self.request.user)

# Retrieve, Update, or Delete a Nutrition Log
class NutritionLogDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NutritionLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Restrict access to only the user’s own logs
        return NutritionLog.objects.filter(user=self.request.user)
