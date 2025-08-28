from django.urls import path
from .views import (
    ColdShowerLogListView,
    ColdShowerLogCreateView,
    ColdShowerLogDetailView,
    ColdShowerLogUpdateView,
    ColdShowerLogDeleteView,
)

app_name = "coldshowers"

urlpatterns = [
    path("", ColdShowerLogListView.as_view(), name="coldshower_list"),
    path("new/", ColdShowerLogCreateView.as_view(), name="coldshower_new"),
    path("<int:pk>/", ColdShowerLogDetailView.as_view(), name="coldshower_detail"),
    path("<int:pk>/edit/", ColdShowerLogUpdateView.as_view(), name="coldshower_edit"),
    path("<int:pk>/delete/", ColdShowerLogDeleteView.as_view(), name="coldshower_delete"),
]
