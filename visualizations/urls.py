from django.urls import path
from .views import VisualizationListCreateAPI, VisualizationDetailAPI

urlpatterns = [
    path('', VisualizationListCreateAPI.as_view(), name='visualizations-list'),
    path('<int:pk>/', VisualizationDetailAPI.as_view(), name='visualizations-detail'),
]
