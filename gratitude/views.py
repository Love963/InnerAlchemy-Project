from django.shortcuts import render
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import GratitudeEntry
from .serializers import GratitudeEntrySerializer

# Create your views here.
class GratitudeListCreateAPI(generics.ListCreateAPIView):
    serializer_class = GratitudeEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tags', 'date']    
    search_fields = ['content', 'tags']      
    ordering_fields = ['date', 'gratitude_score', 'created_at']
    ordering = ['-date']                     

    def get_queryset(self):
        return GratitudeEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GratitudeDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GratitudeEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GratitudeEntry.objects.filter(user=self.request.user)
