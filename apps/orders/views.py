from decimal import Decimal
from reportlab.lib.enums import TA_RIGHT
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q, F
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
from reportlab.platypus import Image, SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
import os

from .models import Product, ProductCategory, Order
from .forms import ProductForm


# ── Products ───────────────────────────────────────────────────────────────────

@login_required
def product_list(request):
    search = request.GET.get('q', '')
    category = request.GET.get('category', '')
    products = Product.objects.select_related('preferred_supplier').filter(active=True)
    orders = Order.objects.all()

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
        'orders': orders,
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


@login_required
def print_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="order_{order.number}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()

    elementos = []

    # 🏫 LOGO
    logo_path = os.path.join("static", "img", "logovan.jpg")
    if os.path.exists(logo_path):
        elementos.append(Image(logo_path, width=80, height=80))

    # 🧾 ENCABEZADO
    doc_id = f"ADP-RQS-{datetime.now().strftime('%d%m%Y')}-{order.number[9:13]}-IFA"


    elementos.append(Paragraph("<b>Vanguard Foundation - PURCHASE ORDER</b>", styles['Title']))
    elementos.append(Spacer(1, 10))

    # 📄 INFO GENERAL
    elementos.append(Paragraph(f"<b><spam>Document Code:</spam></b> {doc_id}", styles['Italic']))
    elementos.append(Paragraph(f"<b>Code:</b> {order.number}", styles['Normal']))
    elementos.append(Paragraph(f"<b>Status:</b> {order.get_status_display()}", styles['Normal']))
    elementos.append(Paragraph(f"<b>Requested by:</b> {order.requested_by}", styles['Normal']))
    elementos.append(Paragraph(f"<b>Date:</b> {order.requested_at.strftime('%d/%m/%Y')}", styles['Normal']))

    if order.required_by:
        elementos.append(Paragraph(f"<b>Required for:</b> {order.required_by}", styles['Normal']))

    elementos.append(Spacer(1, 20))

    # 📦 TABLA DE ITEMS
    data = [[
        "Code", "Product", "Category",
        "Quantity", "Unit", "Supplier","Price", "Subtotal", 
        "Created At"
    ]]

    total = Decimal('0.00')

    items = list(order.items.all())

    for item in items:
        producto = item.product

        precio = producto.reference_price if producto.reference_price else Decimal("0.00")
        subtotal = producto.quantity * precio


        total += subtotal

        data.append([
            producto.code,
            producto.name,
            producto.get_category_display(),
            float(producto.quantity),
            producto.unit,
            producto.preferred_supplier,
            f"${producto.reference_price or 0}",
            f"${Decimal(producto.quantity * (producto.reference_price or 0))}",
            producto.created_at.strftime('%d/%m/%Y'),
        ])

    tabla = Table(data, repeatRows=1)

    tabla.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1f3c88")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

        # Body
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),

        ('ALIGN', (3, 1), (-1, -1), 'CENTER'),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ]))

    elementos.append(tabla)
    elementos.append(Spacer(1, 20))

    # 💰 TOTAL
    right_style = ParagraphStyle(
    name='RightAlign',
    parent=styles['Heading2'],
    alignment=TA_RIGHT)

    elementos.append(Paragraph(f"<b>Total: ${total:.2f}</b>", right_style))

    elementos.append(Spacer(1, 30))

    # 📝 JUSTIFICACIÓN
    if order.justification:
        elementos.append(Paragraph("<b>Justification:</b>", styles['Heading3']))
        elementos.append(Paragraph(order.justification, styles['Normal']))
        elementos.append(Spacer(1, 20))

    # 📝 NOTAS
    if order.notes:
        elementos.append(Paragraph("<b>Observations:</b>", styles['Heading3']))
        elementos.append(Paragraph(order.notes, styles['Normal']))
        elementos.append(Spacer(1, 20))

    # ✍️ FIRMAS
    elementos.append(Paragraph("__________________________", styles['Normal']))
    elementos.append(Paragraph("Requester", styles['Normal']))

    elementos.append(Spacer(1, 20))

    elementos.append(Paragraph("__________________________", styles['Normal']))
    elementos.append(Paragraph("Approval", styles['Normal']))

    # 📌 FOOTER
    elementos.append(Spacer(1, 40))
    elementos.append(Paragraph(
        "Generated on " + datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        styles['Italic']
    ))

    doc.build(elementos)

    return response



