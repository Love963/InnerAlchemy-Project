"""
URL configuration for inneralchemy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Users
    path('users/', include('users.urls', namespace='users')),

    # API v1 endpoints
    
    path('api/v1/breathwork/', include('breathwork.urls', namespace='breathwork')),
    path("api/v1/meditation/", include("meditation.urls")),
    path('api/v1/nutrition/', include('nutrition.urls', namespace='nutrition')),
    path('api/v1/sleep/', include('sleep.urls', namespace='sleep')),
    path('api/v1/solfeggio/', include('solfeggio.urls', namespace='solfeggio')),
    path('api/v1/sexualenergy/', include('sexualenergy.urls', namespace='sexualenergy')),
    path('api/v1/visualizations/', include('visualizations.urls', namespace='visualizations')),
    path('api/v1/gratitude/', include('gratitude.urls', namespace='gratitude')),
    path('api/v1/coldshowers/', include('coldshowers.urls', namespace='coldshowers')),
    path('api/v1/workouts/', include('workouts.urls', namespace='workouts')),
    path('api/v1/soulnotes/', include('soulnotes.urls', namespace='soulnotes')),
    path('api/v1/chakras/', include('chakras.urls', namespace='chakras')),
    path('api/v1/core/', include('core.urls', namespace='core')),
    path('api/v1/habits/', include('habits.urls', namespace='habits')),


    # Dashboard / Core
    path('', include('dashboard.urls')),  # FE dashboard templates
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)