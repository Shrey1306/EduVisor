"""
Views for video upload functionality.
"""

from django.shortcuts import redirect, render

from .forms import VideoUploadForm
from .models import Video


def upload(request):
    """
    Handle lecture video upload.
    
    GET: Display the upload form.
    POST: Process the uploaded video and redirect to preview.
    """
    if request.method == "POST":
        form = VideoUploadForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            video = form.save()
            request.session["lecture_name"] = video.name
            return redirect("uploads:preview")
    else:
        form = VideoUploadForm()
    
    return render(request, "uploads/upload.html", {"form": form})


def preview(request):
    """
    Display uploaded video preview before analysis.
    """
    latest_video = Video.objects.order_by("-id").first()
    
    if not latest_video:
        return redirect("uploads:upload")
    
    context = {
        "video_url": latest_video.video.url,
        "video_name": latest_video.name,
    }
    
    return render(request, "uploads/preview.html", context)

