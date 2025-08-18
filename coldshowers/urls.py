from django.urls import path
from .views import ColdShowerLogListView, ColdShowerLogCreateView, ColdShowerLogDetailView

urlpatterns = [
    path("", ColdShowerLogListView.as_view(), name="coldshower_list"),
    path("new/", ColdShowerLogCreateView.as_view(), name="coldshower_new"),
    path("<int:pk>/", ColdShowerLogDetailView.as_view(), name="coldshower_detail"),
]
