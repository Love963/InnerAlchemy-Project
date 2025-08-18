from django.urls import path
from .views import GratitudeListCreateAPI, GratitudeDetailAPI

urlpatterns = [
    path('', GratitudeListCreateAPI.as_view(), name='gratitude-list'),
    path('<int:pk>/', GratitudeDetailAPI.as_view(), name='gratitude-detail'),
]
