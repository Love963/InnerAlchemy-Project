from django.http import JsonResponse
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import Chakra, ChakraLog
from .serializers import ChakraSerializer, ChakraLogSerializer

# Create your views here.

def index(request):
    return JsonResponse({"message": "Chakras app working!"})


class ChakraViewSet(viewsets.ModelViewSet):
    # ViewSet for Chakra master data (7 main chakras).
    # Public users can list or retrieve.
    # Admins can create/update/delete.
    queryset = Chakra.objects.filter(is_active=True)
    serializer_class = ChakraSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]


class ChakraLogViewSet(viewsets.ModelViewSet):
    # Users can only access their own logs.
    # Supports optional filtering by chakra, state, and date range.
    serializer_class = ChakraLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = ChakraLog.objects.filter(user=user)
        
        # Filter by query parameters
        chakra_param = self.request.query_params.get('chakra')
        state = self.request.query_params.get('state')
        date_from = self.request.query_params.get('date_from')  # fixed typo
        date_to = self.request.query_params.get('date_to')

        if chakra_param:
            if chakra_param.isdigit():
                qs = qs.filter(chakra_id=int(chakra_param))
            else:
                qs = qs.filter(chakra__code=chakra_param)
        if state:
            qs = qs.filter(state=state)
        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)

        return qs

    def perform_create(self, serializer):
        # Automatically assign the current user to the new ChakraLog.
        serializer.save(user=self.request.user)
