from django.urls import path
from .views import GratitudeListCreateAPI, GratitudeDetailAPI

app_name = 'gratitude'
urlpatterns = [
    path('', GratitudeListCreateAPI.as_view(), name='gratitude-list'),
    path('<int:pk>/', GratitudeDetailAPI.as_view(), name='gratitude-detail'),
]
