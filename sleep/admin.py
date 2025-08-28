from django.contrib import admin
from .models import SleepLog, SleepStage, SleepStageType, SleepSolfeggioRecommendation

# Register your models here.
class SleepStageInline(admin.TabularInline):
    model = SleepStage
    extra = 1
    autocomplete_fields = ['stage_type']  


class SleepSolfeggioInline(admin.TabularInline):
    model = SleepSolfeggioRecommendation
    extra = 1


@admin.register(SleepLog)
class SleepLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'total_duration', 'quality_score', 'mood_after')
    list_filter = ('date', 'quality_score')
    search_fields = ('user__username', 'dream_notes', 'rituals')
    ordering = ('-date',)
    inlines = [SleepStageInline, SleepSolfeggioInline]

    fieldsets = (
        ("User & Date", {"fields": ("user", "date")}),
        ("Sleep Info", {"fields": ("sleep_start", "sleep_end", "total_duration", "quality_score", "mood_after")}),
        ("Extras", {"fields": ("rituals", "dream_notes")}),
    )

    readonly_fields = ('total_duration',)


@admin.register(SleepStageType)
class SleepStageTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(SleepStage)
class SleepStageAdmin(admin.ModelAdmin):
    list_display = ('sleep_log', 'stage_type', 'duration_minutes')
    list_filter = ('stage_type',)
    search_fields = ('sleep_log__user__username', 'stage_type__name')


@admin.register(SleepSolfeggioRecommendation)
class SleepSolfeggioRecommendationAdmin(admin.ModelAdmin):
    list_display = ('sleep_log', 'frequency', 'reason')
    search_fields = ('sleep_log__user__username', 'frequency')
