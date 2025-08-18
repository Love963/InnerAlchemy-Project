from django.contrib import admin
from .models import SexualEnergySession, SexualEnergyLog

@admin.register(SexualEnergySession)
class SexualEnergySessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'intention', 'duration_minutes', 'created_at')
    list_filter = ('intention', 'created_at')
    search_fields = ('user__username', 'practice_notes')


@admin.register(SexualEnergyLog)
class SexualEnergyLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'energy_level', 'urges_felt', 'redirect_activity', 'logged_at')
    list_filter = ('energy_level', 'urges_felt', 'logged_at')
    search_fields = ('user__username', 'reflection')
