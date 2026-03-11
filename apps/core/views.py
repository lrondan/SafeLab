from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F
from apps.inventory.models import Campus, Laboratory, Equipment, Reagent, Glassware, Component
from apps.orders.models import Supplier,Product, Order, OrderItem
from apps.reports.models import Report
from django.utils import timezone
from datetime import timedelta

# Create your views here.
@login_required
def dashboard(request):
    today = timezone.now().date()
    return render(request, 'core/dash.html', {
        'stats': {
            'campuses':    Campus.objects.filter().count(),
            'labs':        Laboratory.objects.filter().count(),
            'reagents':    Reagent.objects.filter().count(),
            'equipment':   Equipment.objects.filter().count(),
            'pending':     Report.objects.filter().count(),
            'report':      Report.objects.all()
        }, 
        'recent_breakages': Report.objects.select_related().order_by('reported_at')[:5],
        'expiring':    Reagent.objects.filter(
        ).select_related('laboratory').order_by('updated_at')[:5],

    })