"""
URL configuration for analysis app.
"""

from django.urls import path

from . import views

app_name = "analysis"

urlpatterns = [
    path("", views.analyze, name="analyze"),
    path("loading/", views.loading, name="loading"),
]

