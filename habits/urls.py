from django.urls import path
from .import views

app_name = "habits"

urlpatterns = [
    path('', views.HabitListCreateView.as_view(), name="habit-list"),
    path('<int:pk>/', views.HabitDetailView.as_view(), name="habit-detail"),
    path('logs/', views.HabitLogListCreateView.as_view(), name="habit-log"),
]
