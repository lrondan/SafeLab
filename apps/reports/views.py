from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Report


def report(request):
    if request.method == 'POST':
        student_name = request.POST.get('student_name', '').strip()
        student_id = request.POST.get('student_id', '').strip()
        item_name = request.POST.get('item_name', '').strip()
        quantity = request.POST.get('quantity', 1)
        severity = request.POST.get('severity', 'minor')
        description = request.POST.get('description', '').strip()

        errors = []
        if not student_name:
            errors.append('Your name is required.')
        if not item_name:
            errors.append('Item name is required.')
        try:
            quantity = int(quantity)
            if quantity < 1:
                raise ValueError
        except (ValueError, TypeError):
            errors.append('Quantity must be a positive number.')

        if errors:
            return render(request, 'reports/report.html', {
                'errors': errors,
                'data': request.POST,
            })

        Report.objects.create(
            student_name=student_name,
            student_id=student_id,
            item_name=item_name,
            quantity=quantity,
            severity=severity,
            description=description,
        )
        return redirect('reports:success')

    return render(request, 'reports/report.html')


def success(request):
    return render(request, 'reports/success.html')