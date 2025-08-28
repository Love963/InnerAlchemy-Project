from django.urls import path
from .views import SleepLogListCreateAPI, SleepLogDetailAPI

app_name = 'sleep'
urlpatterns = [
    path('', SleepLogListCreateAPI.as_view(), name='sleep-list-create'),
    path('', SleepLogDetailAPI.as_view(), name='sleep-detail'),
]
