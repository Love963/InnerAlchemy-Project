from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import index, ChakraViewSet, ChakraLogViewSet

router = DefaultRouter()
router.register(r'master', ChakraViewSet, basename='chakra-master')
router.register(r'logs', ChakraLogViewSet, basename='chakra-logs')

urlpatterns = router.urls
app_name = 'chakras'
urlpatterns = [
    path('', index, name='chakras-index'),
    path('', include(router.urls)),
]


