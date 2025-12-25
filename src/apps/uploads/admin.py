"""
Admin configuration for uploads app.
"""

from django.contrib import admin

from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """Admin interface for Video model."""
    
    list_display = ("name", "uploaded_at", "video")
    list_filter = ("uploaded_at",)
    search_fields = ("name",)
    readonly_fields = ("uploaded_at",)

