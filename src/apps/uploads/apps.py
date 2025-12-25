"""
App configuration for uploads module.
"""

from django.apps import AppConfig


class UploadsConfig(AppConfig):
    """Configuration for the uploads app."""
    
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.uploads"
    verbose_name = "Video Uploads"

