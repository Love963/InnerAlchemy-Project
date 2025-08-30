from django.urls import path, include
from .views import UserActivityListCreateAPIView, DashboardAPIView, SummaryReportViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"summaries", SummaryReportViewSet, basename="summary")

app_name = 'core'

urlpatterns = [
    path("", include(router.urls)),
    path('activities/', UserActivityListCreateAPIView.as_view(), name='user-activities'),
    path('dashboard/', DashboardAPIView.as_view(), name='dashboard'),
]




