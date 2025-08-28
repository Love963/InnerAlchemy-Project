from django.contrib import admin
from .models import NutritionLog
# Register your models here.
@admin.register(NutritionLog)
class NutritionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'meal_type', 'calories', 'hydration_liters', 'date')
    list_filter = ('meal_type', 'date')
    search_fields = ('user__username', 'food_items', 'supplements')