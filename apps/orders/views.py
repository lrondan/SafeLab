from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q, F

from .models import Product, ProductCategory
from .forms import ProductForm


# ── Products ───────────────────────────────────────────────────────────────────

@login_required
def product_list(request):
    search = request.GET.get('q', '')
    category = request.GET.get('category', '')
    products = Product.objects.select_related('preferred_supplier').filter(active=True)

    if search:
        products = products.filter(Q(name__icontains=search) | Q(code__icontains=search))
    if category:
        products = products.filter(category=category)
    if request.GET.get('low_stock'):
        products = products.filter(current_stock__lte=F('min_stock'))

    return render(request, 'orders/product_list.html', {
        'products': products,
        'categories': ProductCategory.choices,
        'search': search,
        'selected_category': category,
    })


@login_required
@permission_required('orders.add_product', raise_exception=True)
def create_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        product = form.save()
        messages.success(request, f'Product "{product.name}" created.')
        return redirect('orders:product_list')
    return render(request, 'orders/product_form.html', {'form': form, 'title': 'New Product'})


@login_required
@permission_required('orders.change_product', raise_exception=True)
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        messages.success(request, 'Product updated.')
        return redirect('orders:product_list')
    return render(request, 'orders/product_form.html', {
        'form': form, 'product': product, 'title': 'Edit Product'
    })


