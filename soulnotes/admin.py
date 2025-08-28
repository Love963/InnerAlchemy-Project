from django.contrib import admin
from .models import SoulNote

@admin.register(SoulNote)
class SoulNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'mood', 'date_created')  
    list_filter = ('date_created', 'mood')  
