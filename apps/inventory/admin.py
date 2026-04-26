from django.contrib import admin
from .models import Campus, Laboratory, Equipment, Reagent, Glassware, Component, OtherItem, SafeMaterial, ProcessTrainer


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
    list_display = ('name', 'model_name', 'serial_number', 'quantity' ,'laboratory', 'status')
    list_filter = ('name',)
    search_fields = ('name', 'model_name', 'serial_number')

@admin.register(Reagent)
class ReagentAdmin(admin.ModelAdmin):
    list_display = ('common_name', 'formula', 'quantity', 'unit','laboratory', 'cas_number', 'pubchem_cid', 'status')
    list_filter = ('common_name',)
    search_fields = ('common_name', 'cas_number')

@admin.register(Glassware)
class GlasswareAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','volume', 'quantity', 'laboratory', 'status')
    list_filter = ('laboratory',)
    search_fields = ('name',)

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','quantity','laboratory', 'status')
    list_filter = ('laboratory',)
    search_fields = ('name',)

@admin.register(SafeMaterial)
class SafeMaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'quantity', 'unit', 'laboratory')
    list_filter = ('laboratory',)
    search_fields = ('name',)

@admin.register(OtherItem)
class OtherItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'quantity', 'status', 'laboratory')
    list_filter = ('laboratory',)
    search_fields = ('name',)

@admin.register(ProcessTrainer)
class ProcessTrainerAdmin(admin.ModelAdmin):
    list_display = ('model', 'serial_number','quantity','description', 'laboratory')
    list_filter = ('laboratory', 'model', 'serial_number')
    search_fields = ('model', 'serial_number')
    readonly_fields = ('serial_number',)