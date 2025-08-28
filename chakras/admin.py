from django.contrib import admin
from .models import Chakra, ChakraLog

# Register your models here.
@admin.register(Chakra)
class ChakraAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'sanskrit_name', 'color', 'element', 'is_active')
    list_filter = ('is_active', 'element')
    search_fields = ('name', 'sanskrit_name', 'code')
@admin.register(ChakraLog)
class ChakraLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'chakra', 'state', 'intensity', 'date', 'created_at')
    list_filter = ('state', 'date', 'chakra')
    search_fields = ('user_email', 'user_username', 'notes' )
    