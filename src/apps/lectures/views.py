"""
Views for lecture history.
"""

from django.shortcuts import render

from .models import Lecture


def history(request):
    """
    Display lecture analysis history.
    """
    lectures = Lecture.objects.all()
    return render(request, "lectures/history.html", {"lectures": lectures})

