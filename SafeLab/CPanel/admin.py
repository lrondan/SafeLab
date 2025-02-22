from django.contrib import admin
from .models import Aparatu, ChemSub, glaswerk, Other, safety

# Register your models here.
admin.site.register(Aparatu)
admin.site.register(ChemSub)
admin.site.register(glaswerk)
admin.site.register(safety)
admin.site.register(Other)
