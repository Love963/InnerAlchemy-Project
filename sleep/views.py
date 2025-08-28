from django.shortcuts import render
from .models import SleepLog
from rest_framework import generics, permissions
from .serializers import SleepLogSerializer

# Create your views here.
class SleepLogListCreateAPI(generics.ListCreateAPIView):
    serializer_class = SleepLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SleepLog.objects.filter(user=self.request.user).order_by('-date')
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
class SleepLogDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SleepLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SleepLog.objects.filter(user=self.request.user)
    
    

    