"""
URL configuration for uploads app.
"""

from django.urls import path

from . import views

app_name = "uploads"

urlpatterns = [
    path("", views.upload, name="upload"),
    path("preview/", views.preview, name="preview"),
]

