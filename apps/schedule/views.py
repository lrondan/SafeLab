import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import LabSession


# ── main grid ────────────────────────────────────────────────────

@login_required
def schedule(request):
    return render(request, 'schedules/schedule.html', {
        'sessions': {
        'count':         LabSession.objects.all().order_by('day'),
        }
    })