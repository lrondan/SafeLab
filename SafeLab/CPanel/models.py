from django.db import models
import datetime

# Create your models here.
class Aparatu(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    mark = models.CharField(max_length=50)
    range = models.CharField(max_length=50)
    cant = models.IntegerField()
    Observation = models.TextField()
    date = models.DateField(default=datetime.date.today)
    
    def __str__(self):
        return f"{self.name}, {self.cant}, {self.Observation}"
    

class ChemSub(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    vol = models.IntegerField()
    container = models.IntegerField()
    location = models.CharField(max_length=50)
    Observation = models.TextField()
    date = models.DateField(default=datetime.date.today)
    
    def __str__(self):
        return f"{self.name}, {self.vol}, {self.Observation}"
    
class glaswerk(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    vol = models.IntegerField()
    container = models.IntegerField()
    Observation = models.TextField()
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.name}, {self.container}, {self.Observation}"
    
class Other(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    vol = models.IntegerField()
    container = models.IntegerField()
    Observation = models.TextField()
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.name}, {self.container}, {self.Observation}"
    
class safety(models.Model):
    item = models.CharField(max_length=50, blank=False, null=False)
    mark = models.CharField(max_length=50)
    range = models.IntegerField()
    container = models.IntegerField()    
    Observation = models.TextField()
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.item}, {self.container}, {self.Observation}"