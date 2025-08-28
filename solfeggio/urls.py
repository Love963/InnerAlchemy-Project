from rest_framework.routers import DefaultRouter
from .views import SolfeggioFrequencyViewSet, solfeggio_list
from django.urls import path

app_name = 'solfeggio'
router = DefaultRouter()
router.register(r'frequencies', SolfeggioFrequencyViewSet, basename='solfeggio')

urlpatterns = [
    path('', solfeggio_list, name='solfeggio_list'),
]

urlpatterns += router.urls
