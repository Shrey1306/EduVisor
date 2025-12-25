"""
Models for lecture analysis history.
"""

from django.db import models


class Lecture(models.Model):
    """
    Stores analysis results for a processed lecture.
    
    Attributes:
        name: Title of the lecture.
        created_at: When the analysis was performed.
        engagement_ratio: Percentage of engaging speech segments.
        tone_modality: Score indicating vocal variety.
        questions: Number of questions asked.
        wpm: Words per minute speaking rate.
        suggestion: AI-generated improvement feedback.
        graph: HTML for the engagement timeline visualization.
    """
    
    name = models.CharField(
        max_length=256,
        default="Previous Lecture",
        help_text="Title of the lecture",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the analysis was performed",
    )
    engagement_ratio = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        help_text="Percentage of engaging segments (0-100)",
    )
    tone_modality = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        help_text="Tone modulation score (0-100)",
    )
    questions = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        help_text="Number of questions asked",
    )
    wpm = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        default=0,
        help_text="Words per minute",
    )
    suggestion = models.TextField(
        default="",
        help_text="AI-generated improvement suggestions",
    )
    graph = models.TextField(
        blank=True,
        null=True,
        help_text="HTML for engagement timeline chart",
    )
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Lecture Analysis"
        verbose_name_plural = "Lecture Analyses"
    
    def __str__(self) -> str:
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"

