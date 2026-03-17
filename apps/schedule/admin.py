from django.contrib import admin
from .models import LabSession, SchedulePeriod

# Register your models here.
@admin.register(SchedulePeriod)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ['name','start_date','end_date','active']

@admin.register(LabSession)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['period', 'activity', 'laboratory', 'day', 'professor']