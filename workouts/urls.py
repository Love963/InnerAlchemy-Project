from django.urls import path
from .views import WorkoutListCreateAPIView, WorkoutDetailAPIView

app_name = 'workouts'
urlpatterns = [
    path('', WorkoutListCreateAPIView.as_view(), name='workout-list-create'),
    path('<int:pk>/', WorkoutDetailAPIView.as_view(), name='workout-detail'),
]
