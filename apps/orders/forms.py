from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderItem, Product, Supplier


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['supplier', 'required_by', 'justification', 'notes']
        widgets = {
            'required_by': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'justification': forms.Textarea(attrs={
                'rows': 3, 'class': 'form-control',
                'placeholder': 'Reason for this order...'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 2, 'class': 'form-control',
                'placeholder': 'Additional notes...'
            }),
            'supplier': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'supplier': 'Supplier',
            'required_by': 'Required By',
            'justification': 'Justification',
            'notes': 'Notes',
        }


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'unit_price', 'notes']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select product-select'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control', 'min': '0.01', 'step': '0.01', 'placeholder': '0'
            }),
            'unit_price': forms.NumberInput(attrs={
                'class': 'form-control', 'min': '0', 'step': '0.01', 'placeholder': '0.00'
            }),
            'notes': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Specifications...'
            }),
        }
        labels = {
            'product': 'Product',
            'quantity': 'Quantity',
            'unit_price': 'Unit Price',
            'notes': 'Specifications',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(active=True).order_by('name')
        self.fields['unit_price'].required = False


OrderItemFormSet = inlineformset_factory(
    Order, OrderItem,
    form=OrderItemForm,
    extra=1, can_delete=True, min_num=1, validate_min=True,
)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'code', 'name', 'description', 'category', 'quantity', 'unit',
            'preferred_supplier', 'reference_price', 'min_stock',
            'current_stock', 'requires_approval', 'active'
        ]
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.01', 'step': '0.01'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'preferred_supplier': forms.Select(attrs={'class': 'form-select'}),
            'reference_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'min_stock': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'current_stock': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact', 'email', 'phone', 'address', 'active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class OrderFilterForm(forms.Form):
    status = forms.ChoiceField(
        choices=[('', 'All statuses')] + list(Order._meta.get_field('status').choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search orders...'})
    )