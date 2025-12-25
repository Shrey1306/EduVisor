"""
URL configuration for EduVisor.

Routes:
    /           - Video upload
    /analysis/  - Lecture analysis
    /lectures/  - Lecture history
    /admin/     - Django admin
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.uploads.urls")),
    path("analysis/", include("apps.analysis.urls")),
    path("lectures/", include("apps.lectures.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

