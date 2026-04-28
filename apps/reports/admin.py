from django.contrib import admin
from .models import Report
# Register your models here.

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'item_name', 'severity', 'reported_at', 'resolved')
    list_filter = ('severity', 'reported_at', 'resolved')
    search_fields = ('student_name', 'item_name', 'description')
    ordering = ('-reported_at',)
