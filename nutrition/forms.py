from django import forms
from .models import NutritionLog

class NutritionLogForm(forms.ModelForm):
    class Meta:
        model = NutritionLog
        fields = ['meal_type', 'food_items', 'calories', 'hydration_liters',
                  'supplements', 'energy_effect', 'mood_effect', 'notes']
