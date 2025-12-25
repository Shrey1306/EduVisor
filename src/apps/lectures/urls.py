"""
URL configuration for lectures app.
"""

from django.urls import path

from . import views

app_name = "lectures"

urlpatterns = [
    path("", views.history, name="history"),
]

