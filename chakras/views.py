from django.http import JsonResponse
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import Chakra, ChakraLog
from.serializers import ChakraSerializer, ChakraLogSerializer
def index(request):
    return JsonResponse({"message": "Chakras app working!"})

class ChakraViewSet(viewsets.ModelViewSet):
    queryset = Chakra.objects.filter(is_active=True)
    serializer_class = ChakraSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
    
class ChakraLogViewSet(viewsets.ModelViewSet):
    serializer_class = ChakraLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = ChakraLog.objects.filter(user=self.request.user)
        chakra_param = self.request.query_params.get('chakra')
        state = self.request.query_params.get('state')
        date_form = self.request.query_params.get('date_form')
        date_to = self.request.query_params.get('date_to')

        if chakra_param:
            # allow both id and code
            if chakra_param.isdigit():
                qs = qs.filter(chakra_id=int(chakra_param))
            else:
                qs = qs.filter(chakra__code=chakra_param)
        if state:
            qs = qs.filter(state=state)
        if date_form:
            qs = qs.filter(date__gte=date_form)
        if date_to:
            qs = qs.filter(date__lte=date_to)
        
        return qs
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    

