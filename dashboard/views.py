from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Import all your models
from breathwork.models import BreathworkSession
from chakras.models import ChakraLog
from sexualenergy.models import SexualEnergySession
from visualizations.models import VisualizationAffirmation
from gratitude.models import GratitudeEntry
from coldshowers.models import ColdShowerLog

@login_required
def home(request):
    user = request.user

    recent_breathwork = BreathworkSession.objects.filter(user=user).order_by('-date')[:5]
    recent_chakras = ChakraLog.objects.filter(user=user).order_by('-date')[:5]
    recent_sexual_energy = SexualEnergySession.objects.filter(user=user).order_by('-created_at')[:5]
    recent_visualizations = VisualizationAffirmation.objects.filter(user=user).order_by('-date_created')[:5]
    recent_gratitude = GratitudeEntry.objects.filter(user=request.user).order_by('-created_at')[:5]
    recent_coldshowers = ColdShowerLog.objects.filter(user=user).order_by('-date')[:5]

    context = {
        "recent_breathwork": recent_breathwork,
        "recent_chakras": recent_chakras,
        "recent_sexual_energy": recent_sexual_energy,
        "recent_visualizations": recent_visualizations,
        "recent_gratitude": recent_gratitude,
        "recent_coldshowers": recent_coldshowers,
    }

    return render(request, 'dashboard/home.html', context)
