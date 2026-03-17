from django.db import models
from django.contrib.auth.models import User
from apps.inventory.models import Laboratory

# Create your models here.
class SchedulePeriod(models.Model):
    name = models.CharField(max_length=100)
    start_date=models.DateField()
    end_date=models.DateField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.name
    
class LabSession(models.Model):
    period = models.ForeignKey(SchedulePeriod, on_delete=models.CASCADE, related_name='sessions')
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE, related_name='sessions')
    day = models.DateField()
    professor = models.CharField(max_length=100, blank=False)
    start_time = models.TimeField()
    end_time = models.TimeField()
    activity = models.CharField(max_length=500, blank=True, help_text='Short description, e.g. "Organic Chemistry"')
    student_count = models.PositiveBigIntegerField(default=0)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='created_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    practice_complete = models.BooleanField(default=False)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return (f"{self.day}"
                f"{self.start_time:%H:%M}-{self.end_time:%H:%M} | "
                f"{self.professor} @ {self.laboratory}")
    
    #validation-----------------------------------------------------------------------
    def clean(self):
        errors = []

        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                errors.append("End time must be after start time.")

    @property
    def duration_minutes(self):
        from datetime import datetime, date
        s = datetime.combine(date.today(), self.start_time)
        e = datetime.combine(date.today(), self.end_time)
        return int((e - s).total_seconds() / 60)