from django.urls import path
from .views import NutritionLogListCreateAPIView, NutritionLogDetailAPIView

app_name = "nutrition"

urlpatterns = [
    # GET: list logs, POST: create log
    path("logs/", NutritionLogListCreateAPIView.as_view(), name="log-list-create"),

    # GET: retrieve log, PUT/PATCH: update log, DELETE: remove log
    path("logs/<int:pk>/", NutritionLogDetailAPIView.as_view(), name="log-detail"),
]
