from django.db import models

class VideoMaterial(models.Model):
    name = models.CharField(max_length=200, verbose_name="Name of the video material")
    description = models.TextField(verbose_name="Description of the usage")
    iframe = models.TextField(
        max_length=1000, 
        verbose_name="Iframe code for the video"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Video Material"
        verbose_name_plural = "Video Materials"