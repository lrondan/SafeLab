from django.contrib import admin
from .models import VideoMaterial


@admin.register(VideoMaterial)
class VideoMaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
