from django.contrib import admin
from .models import MeditationSession

# Register your models here.
@admin.register(MeditationSession)
class MeditationSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'duration_minutes', 'date')
    list_filter = ('date', 'user')
    search_fields = ('title', 'description')