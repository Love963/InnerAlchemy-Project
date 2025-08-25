from django.urls import path
from .views import UserActivityListCreateAPIView, DashboardAPIView

app_name = 'core'

urlpatterns = [
    path('activities/', UserActivityListCreateAPIView.as_view(), name='user-activities'),
    path('dashboard/', DashboardAPIView.as_view(), name='dashboard'),
]
