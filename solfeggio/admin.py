from django.contrib import admin
from .models import SolfeggioFrequency
# Register your models here.

@admin.register(SolfeggioFrequency)
class SolfeggioFrequencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'frequency_hz')
    search_fields = ('name', 'frequency_hz')
