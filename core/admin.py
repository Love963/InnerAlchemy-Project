from django.contrib import admin
from .models import SummaryReport

# Register your models here.

@admin.register(SummaryReport)
class SummaryReportAdmin(admin.ModelAdmin):
    list_display = ("user", "period", "start_date", "end_date", "created_at")
    list_filter = ("period", "start_date", "end_date")
    search_fields = ("user__username", "user__email")
