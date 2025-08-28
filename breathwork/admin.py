from django.contrib import admin
from .models import BreathworkSession

# Register your models here.
@admin.register(BreathworkSession)
class BreathworkSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'technique', 'duration', 'energy_level', 'date')
    list_filter = ('technique', 'date')
    search_fields = ('user__username', 'technique')

    def get_user_email(self, obj):
        return obj.user.emeil
    get_user_email.short_description = 'User Email'
