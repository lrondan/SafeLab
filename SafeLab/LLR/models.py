from django.db import models
import datetime

# Create your models here.
class Register_User(models.Model):
    username = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    password = models.CharField(max_length=50, blank=False, null=False)
    confirm_password = models.CharField(max_length=50, blank=False, null=False)
    date = models.DateField(default=datetime.date.today)
    

    def __str__(self):
        return self.username