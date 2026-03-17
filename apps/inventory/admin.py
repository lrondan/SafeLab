from django.contrib import admin
from .models import Campus, Laboratory, Equipment, Reagent, Glassware, Component


# Register your models here.
admin.site.site_header = "SafeLab Admin"
admin.site.site_title = "SafeLab Admin Portal"

@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'address')
    list_filter = ('state',)
    search_fields = ('name', 'address')

@admin.register(Laboratory)
class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'campus', 'responsible')
    list_filter = ('campus',)
    search_fields = ('name', 'responsible')

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'model_name', 'laboratory', 'quantity', 'serial_number')
    list_filter = ('name',)
    search_fields = ('name', 'model_name', 'serial_number')

@admin.register(Reagent)
class ReagentAdmin(admin.ModelAdmin):
    list_display = ('common_name', 'formula', 'laboratory', 'cas_number')
    list_filter = ('common_name',)
    search_fields = ('common_name', 'cas_number')

@admin.register(Glassware)
class GlasswareAdmin(admin.ModelAdmin):
    list_display = ('name', 'laboratory')
    list_filter = ('laboratory',)
    search_fields = ('name',)

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'laboratory', 'quantity')
    list_filter = ('laboratory',)
    search_fields = ('name',)