from django.contrib import admin
from .models import WorkoutSession

# Register your models here.
@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'duration_minutes', 'energy_effect', 'date')
    list_filter = ('type', 'date')
    search_fields = ('user__username', 'type')