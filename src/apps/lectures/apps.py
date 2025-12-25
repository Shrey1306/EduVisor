"""
App configuration for lectures module.
"""

from django.apps import AppConfig


class LecturesConfig(AppConfig):
    """Configuration for the lectures app."""
    
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.lectures"
    verbose_name = "Lecture History"

