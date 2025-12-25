"""
Models for video upload functionality.
"""

from django.db import models


class Video(models.Model):
    """
    Represents an uploaded lecture video.
    
    Attributes:
        name: Title/topic of the lecture.
        video: The uploaded video file.
        uploaded_at: Timestamp of upload.
    """
    
    name = models.CharField(
        max_length=256,
        default="Untitled Lecture",
        help_text="Title or topic of the lecture",
    )
    video = models.FileField(
        upload_to="videos/",
        help_text="The lecture video file",
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the video was uploaded",
    )
    
    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Lecture Video"
        verbose_name_plural = "Lecture Videos"
    
    def __str__(self) -> str:
        return f"{self.name} ({self.uploaded_at.strftime('%Y-%m-%d')})"

