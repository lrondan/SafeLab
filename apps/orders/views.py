from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import Order, OrderItem, Product, Supplier, OrderStatus
from .forms import OrderForm, OrderItemFormSet, ProductForm, SupplierForm, OrderFilterForm


@login_required
def dashboard(request):
    from django.db.models import F
    recent_orders = Order.objects.filter(
        requested_by=request.user
    ).select_related('supplier')[:5]

    my_orders_count = Order.objects.filter(requested_by=request.user).count()
    pending_count = Order.objects.filter(status=OrderStatus.PENDING).count()
    in_progress_count = Order.objects.filter(status=OrderStatus.IN_PROGRESS).count()
    low_stock_count = Product.objects.filter(
        active=True, current_stock__lte=F('min_stock')
    ).count()

    return render(request, 'orders/dashboard.html', {
        'recent_orders': recent_orders,
        'my_orders_count': my_orders_count,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'low_stock_count': low_stock_count,
    })


@login_required
def order_list(request):
    filter_form = OrderFilterForm(request.GET)
    orders = Order.objects.select_related(
        'requested_by', 'supplier', 'approved_by'
    ).prefetch_related('items')

    if filter_form.is_valid():
        status = filter_form.cleaned_data.get('status')
        date_from = filter_form.cleaned_data.get('date_from')
        date_to = filter_form.cleaned_data.get('date_to')
        search = filter_form.cleaned_data.get('search')

        if status:
            orders = orders.filter(status=status)
        if date_from:
            orders = orders.filter(requested_at__date__gte=date_from)
        if date_to:
            orders = orders.filter(requested_at__date__lte=date_to)
        if search:
            orders = orders.filter(
                Q(number__icontains=search) |
                Q(justification__icontains=search) |
                Q(supplier__name__icontains=search) |
                Q(requested_by__first_name__icontains=search) |
                Q(requested_by__last_name__icontains=search)
            )

    page_obj = Paginator(orders, 20).get_page(request.GET.get('page'))
    return render(request, 'orders/order_list.html', {
        'page_obj': page_obj,
        'filter_form': filter_form,
    })


@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            order = form.save(commit=False)
            order.requested_by = request.user
            order.status = OrderStatus.DRAFT
            order.save()
            formset.instance = order
            formset.save()
            order.refresh_total()
            messages.success(request, f'Order {order.number} created successfully.')
            return redirect('orders:order_detail', pk=order.pk)
        messages.error(request, 'Please fix the errors below.')
    else:
        form = OrderForm()
        formset = OrderItemFormSet()

    return render(request, 'orders/order_form.html', {
        'form': form,
        'formset': formset,
        'title': 'New Order',
        'products_json': _get_products_json(),
    })


@login_required
def edit_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if not order.can_edit:
        messages.error(request, 'This order cannot be edited.')
        return redirect('orders:order_detail', pk=pk)
    if order.requested_by != request.user and not request.user.has_perm('orders.change_order'):
        messages.error(request, 'You do not have permission to edit this order.')
        return redirect('orders:order_detail', pk=pk)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            order.refresh_total()
            messages.success(request, 'Order updated successfully.')
            return redirect('orders:order_detail', pk=pk)
        messages.error(request, 'Please fix the errors below.')
    else:
        form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)

    return render(request, 'orders/order_form.html', {
        'form': form,
        'formset': formset,
        'order': order,
        'title': f'Edit Order {order.number}',
        'products_json': _get_products_json(),
    })


@login_required
def order_detail(request, pk):
    order = get_object_or_404(
        Order.objects.select_related('requested_by', 'supplier', 'approved_by')
                     .prefetch_related('items__product'),
        pk=pk
    )
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'OrderStatus': OrderStatus,
    })


@login_required
def submit_order(request, pk):
    order = get_object_or_404(Order, pk=pk, requested_by=request.user)
    if order.status != OrderStatus.DRAFT:
        messages.error(request, 'Only draft orders can be submitted.')
        return redirect('orders:order_detail', pk=pk)
    if not order.items.exists():
        messages.error(request, 'Add at least one product before submitting.')
        return redirect('orders:order_detail', pk=pk)
    order.status = OrderStatus.PENDING
    order.save()
    messages.success(request, f'Order {order.number} submitted for approval.')
    return redirect('orders:order_detail', pk=pk)


@login_required
@permission_required('orders.change_order', raise_exception=True)
def approve_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.status != OrderStatus.PENDING:
        messages.error(request, 'Only pending orders can be approved.')
        return redirect('orders:order_detail', pk=pk)
    order.status = OrderStatus.APPROVED
    order.approved_by = request.user
    order.approved_at = timezone.now()
    order.save()
    messages.success(request, f'Order {order.number} approved.')
    return redirect('orders:order_detail', pk=pk)


@login_required
@permission_required('orders.change_order', raise_exception=True)
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = OrderStatus.CANCELLED
    order.save()
    messages.warning(request, f'Order {order.number} has been cancelled.')
    return redirect('orders:order_detail', pk=pk)


@login_required
@permission_required('orders.change_order', raise_exception=True)
def change_order_status(request, pk, new_status):
    order = get_object_or_404(Order, pk=pk)
    valid_statuses = [s[0] for s in OrderStatus.choices]
    if new_status not in valid_statuses:
        messages.error(request, 'Invalid status.')
        return redirect('orders:order_detail', pk=pk)

    order.status = new_status
    if new_status == OrderStatus.RECEIVED:
        order.received_at = timezone.now().date()
        for item in order.items.all():
            item.product.current_stock += item.quantity
            item.product.save()
    order.save()
    messages.success(request, f'Order status updated to: {order.get_status_display()}')
    return redirect('orders:order_detail', pk=pk)


# ── Products ───────────────────────────────────────────────────────────────────

@login_required
def product_list(request):
    from django.db.models import F
    from .models import ProductCategory
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


# ── Suppliers ──────────────────────────────────────────────────────────────────

@login_required
def supplier_list(request):
    suppliers = Supplier.objects.filter(active=True).annotate(
        total_products=Count('products')
    )
    return render(request, 'orders/supplier_list.html', {'suppliers': suppliers})


@login_required
@permission_required('orders.add_supplier', raise_exception=True)
def create_supplier(request):
    form = SupplierForm(request.POST or None)
    if form.is_valid():
        supplier = form.save()
        messages.success(request, f'Supplier "{supplier.name}" created.')
        return redirect('orders:supplier_list')
    return render(request, 'orders/supplier_form.html', {'form': form, 'title': 'New Supplier'})


@login_required
@permission_required('orders.change_supplier', raise_exception=True)
def edit_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    form = SupplierForm(request.POST or None, instance=supplier)
    if form.is_valid():
        form.save()
        messages.success(request, 'Supplier updated.')
        return redirect('orders:supplier_list')
    return render(request, 'orders/supplier_form.html', {
        'form': form, 'supplier': supplier, 'title': 'Edit Supplier'
    })


# ── API ────────────────────────────────────────────────────────────────────────

@login_required
def api_product_info(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return JsonResponse({
        'id': product.pk,
        'name': product.name,
        'code': product.code,
        'unit': product.get_unit_display(),
        'price': float(product.reference_price) if product.reference_price else None,
        'current_stock': float(product.current_stock),
    })


def _get_products_json():
    import json
    return json.dumps([
        {
            'id': p['id'],
            'name': p['name'],
            'code': p['code'],
            'price': float(p['reference_price']) if p['reference_price'] else 0,
            'unit': p['unit'],
        }
        for p in Product.objects.filter(active=True).values(
            'id', 'name', 'code', 'reference_price', 'unit'
        )
    ])
