from django.contrib import admin
from .models import Challenge, ChallengeMembership, ChallengeProgress

# Register your models here.

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ("title", "visibility", "goal_type", "start_date", "end_date", "created_by", "created_at")
    list_filter = ("visibility", "goal_type", "start_date", "end_date")
    search_fields = ("title", "description", "created_by__username")

@admin.register(ChallengeMembership)
class ChallengeMembershipAdmin(admin.ModelAdmin):
    list_display = ("challenge", "user", "status", "joined_at", "left_at")
    list_filter = ("status", "joined_at")
    search_fields = ("challenge__title", "user__username")

@admin.register(ChallengeProgress)
class ChallengeProgressAdmin(admin.ModelAdmin):
    list_display = ("challenge", "user", "date", "value", "created_at")
    list_filter = ("date",)
    search_fields = ("challenge__title", "user__username", "note")
