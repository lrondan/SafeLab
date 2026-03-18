from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem, Product, Supplier


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ['product', 'quantity', 'unit_price', 'notes']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['number', 'requested_by', 'supplier', 'status', 'estimated_total', 'requested_at']
    list_filter = ['status', 'requested_at', 'supplier']
    search_fields = ['number', 'requested_by__username', 'justification']
    readonly_fields = ['number', 'requested_at', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    date_hierarchy = 'requested_at'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields =['code',]
    list_display = ['code', 'name', 'category', 'reference_price', 'current_stock', 'min_stock','active']
    list_filter = ['category', 'active', 'requires_approval']
    search_fields = ['code', 'name', 'description']
    list_editable = ['active']



@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact', 'email', 'phone', 'active']
    list_filter = ['active']
    search_fields = ['name', 'contact', 'email']
    list_editable = ['active']