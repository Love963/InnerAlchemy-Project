from rest_framework.routers import DefaultRouter
from .views import SolfeggioFrequencyViewSet
from django.urls import path
from . import views
router = DefaultRouter()
router.register(r'', SolfeggioFrequencyViewSet, basename='solfeggio')

urlpatterns = router.urls


urlpatterns = [
    path('', views.solfeggio_list, name='solfeggio_list'),
]
