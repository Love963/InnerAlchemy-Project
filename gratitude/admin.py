from django.contrib import admin
from .models import GratitudeEntry
# Register your models here.
@admin.register(GratitudeEntry)
class GratitudeEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'gratitude_score', 'solfeggio_frequency')
    list_filter = ('date', 'solfeggio_frequency')
    search_fields = ('content', 'tags', 'user__username')