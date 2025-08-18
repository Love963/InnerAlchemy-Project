from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import ChakraViewSet, ChakraLogViewSet

router = DefaultRouter()
router.register(r'master', ChakraViewSet, basename='chakra-master')
router.register(r'logs', ChakraLogViewSet, basename='chakra-logs')

urlpatterns = router.urls

urlpatterns = [
    path('', views.index, name='chakras-index'),
]
