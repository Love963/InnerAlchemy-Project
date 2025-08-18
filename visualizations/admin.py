from django.contrib import admin
from .models import VisualizationAffirmation
# Register your models here.
@admin.register(VisualizationAffirmation)
class VisualizationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date_created', 'solfeggio_frequency')
    list_filter = ('date_created', 'solfeggio_frequency')
    search_fields = ('title', 'content', 'tags', 'user_username')