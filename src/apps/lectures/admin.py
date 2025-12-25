"""
Admin configuration for lectures app.
"""

from django.contrib import admin

from .models import Lecture


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    """Admin interface for Lecture model."""
    
    list_display = ("name", "created_at", "engagement_ratio", "tone_modality", "wpm")
    list_filter = ("created_at",)
    search_fields = ("name",)
    readonly_fields = ("created_at", "graph")

