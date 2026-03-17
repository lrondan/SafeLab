from django.db import models
from django.utils import timezone
import pubchempy as pcp

class Campus(models.Model):
    name = models.CharField(max_length=100, unique=True)
    state = models.CharField(max_length=100)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.state}"


class Laboratory(models.Model):
    name = models.CharField(max_length=100)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='laboratories')
    responsible = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} ({self.campus.name})"


class Equipment(models.Model):
    STATUSES = [
        ('good', '✅ Good'),
        ('broken', '❌ Broken'),
        ('repair', '🔧 In Repair'),
        ('borrowed', '📤 Borrowed'),
    ]

    name = models.CharField(max_length=200)
    model_name = models.CharField(max_length=50, blank=True, help_text="Model number or name of the equipment")
    description = models.TextField(blank=True)
    serial_number = models.CharField(max_length=100, unique=True)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUSES, default='good')
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE, related_name='equipments')
    
    purchase_date = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.serial_number}) - {self.get_status_display()}"


class Reagent(models.Model):
    STATUSES = [
        ('available', '✅ Available'),
        ('low', '⚠️ Low Stock'),
        ('out', '❌ Out of Stock'),
        ('expired', '⏰ Expired'),
    ]

    common_name = models.CharField(max_length=200)
    iupac_name = models.CharField(max_length=200, blank=True)
    formula = models.CharField(max_length=100, blank=True)
    molecular_weight = models.FloatField(null=True, blank=True)
    cas_number = models.CharField(max_length=50, blank=True, unique=True)
    
    pubchem_cid = models.PositiveIntegerField(null=True, blank=True, unique=True)
    pubchem_link = models.URLField(blank=True)
    
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=10, choices=[('g', 'g'), ('ml', 'ml')], default='g')
    status = models.CharField(max_length=20, choices=STATUSES, default='available')
    
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE, related_name='reagents')
    updated_at = models.DateTimeField(auto_now=True)
    safety_notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.common_name} ({self.formula}) - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        if self.pubchem_cid and not self.pubchem_link:
            self.pubchem_link = f"https://pubchem.ncbi.nlm.nih.gov/compound/{self.pubchem_cid}#section=Safety-and-Hazards"
        super().save(*args, **kwargs)

class Glassware(models.Model):
    STATUSES = [
        ('good', '✅ Good'),
        ('broken', '❌ Broken'),
        ('repair', '🔧 In Repair'),
        ('borrowed', '📤 Borrowed'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    volume = models.CharField(max_length=50, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUSES, default='good')
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE, related_name='glasswares')
    
    date_purchased = models.DateField(null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, help_text = " Here you can add any additional information about the glassware, such as maintenance history, usage instructions, etc.")

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"
    

class Component(models.Model):
    STATUSES = [
        ('good', '✅ Good'),
        ('broken', '❌ Broken'),
        ('missing', '⚠️ Missing'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUSES, default='good')
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE, related_name='components')
    
    date_added = models.DateField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.laboratory.name}"