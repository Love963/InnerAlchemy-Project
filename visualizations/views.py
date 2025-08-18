from rest_framework import generics, permissions
from .models import VisualizationAffirmation
from .serializers import VisualizationSerializer

class VisualizationListCreateAPI(generics.ListCreateAPIView):
    serializer_class = VisualizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users see only their own visualizations
        return VisualizationAffirmation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VisualizationDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VisualizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only access their own visualizations
        return VisualizationAffirmation.objects.filter(user=self.request.user)
