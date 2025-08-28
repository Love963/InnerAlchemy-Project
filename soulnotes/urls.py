# soulnotes/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SoulNoteViewSet

app_name = 'soulnotes'

router = DefaultRouter()
router.register(r'soul-notes', SoulNoteViewSet, basename='soul-note')

urlpatterns = [
    path('', include(router.urls)), 
]
