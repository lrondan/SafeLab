from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ProductCategory(models.TextChoices):
    CHEMICAL = 'CHEMICAL', 'Chemical'
    COMPONENT = 'COMPONENT', 'Component'
    INSTRUMENT = 'INSTRUMENT', 'Lab Instrument'
    CONSUMABLE = 'CONSUMABLE', 'Consumable'
    REAGENT = 'REAGENT', 'Reagent'


class UnitOfMeasure(models.TextChoices):
    LITER = 'L', 'Liter'
    MILLILITER = 'mL', 'Milliliter'
    GRAM = 'g', 'Gram'
    KILOGRAM = 'kg', 'Kilogram'
    UNIT = 'unit', 'Unit'
    BOX = 'box', 'Box'
    BOTTLE = 'bottle', 'Bottle'


class OrderStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    PENDING = 'PENDING', 'Pending'
    APPROVED = 'APPROVED', 'Approved'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    SHIPPED = 'SHIPPED', 'Shipped'
    RECEIVED = 'RECEIVED', 'Received'
    CANCELLED = 'CANCELLED', 'Cancelled'


class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
        ordering = ['name']


class Product(models.Model):
    AUTOCODE = 'PKG'
    code = models.CharField(max_length=50, blank=True, null=True, help_text='Auto')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(
        max_length=20,
        choices=ProductCategory.choices,
        default=ProductCategory.CHEMICAL
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit = models.CharField(
        max_length=10,
        choices=UnitOfMeasure.choices,
        default=UnitOfMeasure.UNIT
    )
    preferred_supplier = models.ForeignKey(
        Supplier, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='products'
    )
    reference_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    min_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    requires_approval = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.code}] {self.name}"

    @property
    def needs_restock(self):
        return self.current_stock <= self.min_stock
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.code:
            self.code = f"{self.AUTOCODE}{self.id}"
            super().save(update_fields=['code'])

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']


class Order(models.Model):
    number = models.CharField(max_length=20, unique=True, editable=False)
    requested_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='requested_orders'
    )
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='approved_orders'
    )
    supplier = models.ForeignKey(
        Supplier, on_delete=models.SET_NULL, null=True, blank=True
    )
    status = models.CharField(
        max_length=20, choices=OrderStatus.choices, default=OrderStatus.DRAFT
    )
    requested_at = models.DateTimeField(default=timezone.now)
    required_by = models.DateField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    received_at = models.DateField(null=True, blank=True)
    justification = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    estimated_total = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.number} - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        if not self.number:
            last = Order.objects.order_by('-id').first()
            next_id = (last.id + 1) if last else 1
            self.number = f"ORD-{timezone.now().year}-{next_id:04d}"
        super().save(*args, **kwargs)
        self.refresh_total()

    def refresh_total(self):
        total = sum(
            item.subtotal for item in self.items.all() if item.subtotal is not None
        )
        Order.objects.filter(pk=self.pk).update(estimated_total=total)

    @property
    def can_edit(self):
        return self.status in [OrderStatus.DRAFT, OrderStatus.PENDING]

    @property
    def can_approve(self):
        return self.status == OrderStatus.PENDING

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-requested_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    notes = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

    @property
    def subtotal(self):
        if self.unit_price:
            return self.quantity * self.unit_price
        return None

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        unique_together = ('order', 'product')