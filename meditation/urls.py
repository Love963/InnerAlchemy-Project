# meditation/urls.py
from django.urls import path
from .views import MeditationSessionListCreateView, MeditationSessionDetailView

app_name = "meditation"

urlpatterns = [
    path("sessions/", MeditationSessionListCreateView.as_view(), name="meditation-list-create"),
    path("sessions/<int:pk>/", MeditationSessionDetailView.as_view(), name="meditation-detail"),
]
