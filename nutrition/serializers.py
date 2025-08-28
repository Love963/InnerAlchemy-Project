from rest_framework import serializers
from .models import NutritionLog

class NutritionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionLog
        fields = [
            "id",
            "user",
            "meal_type",
            "food_items",     
            "calories",
            "hydration_liters",
            "supplements",
            "energy_effect",
            "mood_effect",
            "notes",
            "date",
            "nutrition_score",    
        ]
        read_only_fields = ["id", "user", "nutrition_score"]
