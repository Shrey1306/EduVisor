"""
Views for lecture analysis.
"""

from pathlib import Path

from django.conf import settings
from django.shortcuts import render

from apps.uploads.models import Video
from apps.lectures.models import Lecture
from core.services import LectureAnalyzer


def loading(request):
    """Display loading page while analysis runs."""
    return render(request, "analysis/loading.html")


def analyze(request):
    """
    Analyze the most recently uploaded lecture video.
    
    Performs comprehensive analysis including:
    - Speech emotion recognition
    - Transcript generation
    - Engagement metrics
    - AI-generated feedback
    """
    latest_video = Video.objects.order_by("-id").first()
    if not latest_video:
        return render(request, "analysis/results.html", {"error": "No video found"})
    
    video_path = settings.MEDIA_ROOT / str(latest_video.video)
    
    # Run analysis
    analyzer = LectureAnalyzer()
    result = analyzer.analyze(video_path)
    
    # Get lecture name from session
    lecture_name = request.session.get("lecture_name", "Lecture").title()
    
    # Save to database
    lecture = Lecture.objects.create(
        name=lecture_name,
        engagement_ratio=result.metrics.engagement_percentage,
        tone_modality=result.metrics.tone_modulation_score,
        questions=result.metrics.question_count,
        wpm=result.metrics.words_per_minute,
        suggestion=result.feedback,
        graph=result.timeline_chart_html,
    )
    
    # Build template context
    context = result.to_context()
    context["name"] = lecture_name
    context["date"] = lecture.created_at.strftime("%Y-%m-%d")
    
    return render(request, "analysis/results.html", context)

