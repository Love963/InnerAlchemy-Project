from rest_framework import generics, permissions, filters
from .models import VisualizationAffirmation
from .serializers import VisualizationSerializer

# Create your views here.
class VisualizationListCreateAPI(generics.ListCreateAPIView):
    # List all affirmations for the logged-in user,  or create a new affirmation entry.
    serializer_class = VisualizationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content", "tags__name"]
    ordering_fields = ["date_created", "updated_at"]

    def get_queryset(self):
        queryset = VisualizationAffirmation.objects.filter(user=self.request.user)

        # Optional filtering by query params
        tag = self.request.query_params.get("tag")
        freq = self.request.query_params.get("frequency")

        if tag:
            queryset = queryset.filter(tags__name__iexact=tag)
        if freq:
            queryset = queryset.filter(solfeggio_frequency__id=freq)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VisualizationDetailAPI(generics.RetrieveUpdateDestroyAPIView):

    # Retrieve, update, or delete a specific affirmation.
    # Users can only interact with their own affirmations.
    serializer_class = VisualizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VisualizationAffirmation.objects.filter(user=self.request.user)
