from django.urls import path
from .views import BreathworkSessionListCreateAPIView, BreathworkSessionDetailAPIView

urlpatterns = [
    path('sessions/', BreathworkSessionListCreateAPIView.as_view(), name='breathwork-list-create'),
    path('sessions/<int:pk>/', BreathworkSessionDetailAPIView.as_view(), name='breathwork-detail'),
]
