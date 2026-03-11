from django.shortcuts import render
from .models import VideoMaterial

def gallery(request):
    materials = VideoMaterial.objects.all().order_by('-created_at')

    return render(request, 'gallery/gallery.html', 
                  {'materials': materials})