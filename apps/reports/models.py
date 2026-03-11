from django.db import models

# Create your models here.
class Report(models.Model):
    SEVERITY_CHOICES = [
        ('minor', 'Minor - small crack or chip'),
        ('moderate', 'Moderate - Partially broken, still usable'),
        ('severe', 'Severe - Fully broken, not usable'),
    ]

    student_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20)
    item_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    description = models.TextField(blank=True)
    reported_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student_name} - {self.item_name} ({self.severity})"
    
    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'