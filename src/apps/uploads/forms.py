"""
Forms for video upload functionality.
"""

from django import forms

from .models import Video


class VideoUploadForm(forms.ModelForm):
    """Form for uploading lecture videos."""
    
    name = forms.CharField(
        label="Lecture Topic",
        max_length=256,
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "Enter lecture topic",
        }),
    )
    
    video = forms.FileField(
        label="Video File",
        widget=forms.ClearableFileInput(attrs={
            "class": "form-input",
            "accept": "video/*",
        }),
    )
    
    class Meta:
        model = Video
        fields = ("name", "video")

