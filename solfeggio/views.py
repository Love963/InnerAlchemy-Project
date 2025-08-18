from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import SolfeggioFrequency
from .serializers import SolfeggioFrequencySerializer
# Create your views here.

class SolfeggioFrequencyViewSet(viewsets.ModelViewSet):
    """
    Master Solfeggio frequencies.
    - Anyone can list/retrieve
    - Only admin can create/update/delete
    """
    queryset = SolfeggioFrequency.objects.all()
    serializer_class = SolfeggioFrequencySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

def solfeggio_list(request):
    frequencies = SolfeggioFrequency.objects.all()
    return render(request, 'solfeggio/solfeggio_list.html', {'frequencies': frequencies})

