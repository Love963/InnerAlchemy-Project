from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ChallengeViewSet, ChallengeProgressViewSet

app_name = "challenges"

router = DefaultRouter()
router.register(r"challenges", ChallengeViewSet, basename="challenge")
router.register(r"progress", ChallengeProgressViewSet, basename="challenge-progress")

urlpatterns = [
    path("", include(router.urls)),
]
