from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.inventory.models import Equipment, Reagent, Glassware, Component
from apps.schedule.models import LabSession
from apps.reports.models import Report
from django.utils import timezone
from datetime import timedelta

# Create your views here.
@login_required
def dashboard(request):
    today = timezone.now().date()
    report_count = Report.objects.count()
    report_solved = Report.objects.filter(resolved='True').count()
    return render(request, 'core/dash.html', {
        'stats': {
            'practicals': LabSession.objects.filter(practice_complete = False).count(),
            'solved_rep':  ((report_solved/report_count) * 100).__int__ if report_count else 0,
            'reagents':    Reagent.objects.filter().count(),
            'equipment':   Equipment.objects.filter().count(),
            'pending':     Report.objects.filter(resolved=False).count(),
            'report':      Report.objects.all(),
            'glassware':   Glassware.objects.filter().count(),
            'component':   Component.objects.filter().count(),
        }, 
        'recent_breakages': Report.objects.select_related().order_by('reported_at')[:5],
        'expiring':    Reagent.objects.filter().select_related('laboratory').order_by('updated_at')[:5],

    })