from django.urls import path
from . import views

app_name = 'sexualenergy'
urlpatterns = [
    path('dashboard/', views.energy_dashboard, name='dashboard'),
    path("sessions/", views.SexualEnergySessionListView.as_view(), name="session_list"),
    path("sessions/<int:pk>/", views.SexualEnergySessionDetailView.as_view(), name="session_detail"),
    path("sessions/create/", views.SexualEnergySessionCreateView.as_view(), name="session_create"),
    path("sessions/<int:pk>/update/", views.SexualEnergySessionUpdateView.as_view(), name="session_update"),
    path("sessions/<int:pk>/delete/", views.SexualEnergySessionDeleteView.as_view(), name="session_delete"),

    # Logs
    path("logs/", views.SexualEnergyLogListView.as_view(), name="log_list"),
    path("logs/<int:pk>/", views.SexualEnergyLogDetailView.as_view(), name="log_detail"),
    path("logs/create/", views.SexualEnergyLogCreateView.as_view(), name="log_create"),
    path("logs/<int:pk>/update/", views.SexualEnergyLogUpdateView.as_view(), name="log_update"),
    path("logs/<int:pk>/delete/", views.SexualEnergyLogDeleteView.as_view(), name="log_delete"),
]
