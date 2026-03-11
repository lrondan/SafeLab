from urllib import request

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Campus, Laboratory, Equipment, Reagent, Glassware, Component
from .forms import EquipmentForm, ReagentForm, GlasswareForm, ComponentForm
import pubchempy as pcp
from django.core.paginator import Paginator

from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter
from datetime import datetime


@login_required
def home(request):
    """Main page: list of all campuses."""
    campuses = Campus.objects.all()
    return render(request, 'inventory/home.html', {'campuses': campuses})


@login_required
def campus_detail(request, campus_id):
    """Show all laboratories in a campus."""
    campus = get_object_or_404(Campus, id=campus_id)
    laboratories = campus.laboratories.all()
    return render(request, 'inventory/campus_detail.html', {
        'campus': campus,
        'laboratories': laboratories
    })


@login_required
def lab_detail(request, lab_id):
    """Laboratory detail with Equipment and Reagents (Bootstrap tabs)."""
    lab = get_object_or_404(Laboratory, id=lab_id)

    # Equipment
    equipments = lab.equipments.all().order_by('name')
    equipment_status = request.GET.get('equipment_status')
    if equipment_status:
        equipments = equipments.filter(status=equipment_status)

    # Reagents
    reagents = lab.reagents.all().order_by('common_name')
    reagent_status = request.GET.get('reagent_status')
    if reagent_status:
        reagents = reagents.filter(status=reagent_status)

    #glassware
    glasswares = lab.glasswares.all().order_by('name')
    glassware_status = request.GET.get('glassware_status')
    if glassware_status:
        glasswares = glasswares.filter(status=glassware_status)

    #components
    components = lab.components.all().order_by('name')
    component_status = request.GET.get('component_status')
    if component_status:
        components = components.filter(status=component_status)

    def paginate(qs, param):
        return Paginator(qs, 10).get_page(request.GET.get(param))

    equipments = paginate(equipments, 'equipments_page')
    reagents = paginate(reagents, 'reagents_page')
    glasswares = paginate(glasswares, 'glasswares_page')
    components = paginate(components, 'components_page')

    return render(request, 'inventory/lab_detail.html', {
        'lab': lab,
        'equipments': equipments,
        'reagents': reagents,
        'glasswares': glasswares,
        'components': components,
        'equipment_statuses': Equipment.STATUSES,
        'reagent_statuses': Reagent.STATUSES,
        'glassware_statuses': Glassware.STATUSES,
        'component_statuses': Component.STATUSES,
    })


@login_required
def equipment_create(request, lab_id):
    """Create new equipment."""
    lab = get_object_or_404(Laboratory, id=lab_id)
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.laboratory = lab
            equipment.save()
            return redirect('lab_detail', lab_id=lab.id)
    else:
        form = EquipmentForm()

    return render(request, 'inventory/equipment_form.html', {
        'form': form,
        'lab': lab,
        'title': 'New Equipment'
    })

@login_required
def equipment_update(request, equipment_id):
    """Update equipment (e.g. mark as Broken)."""
    equipment = get_object_or_404(Equipment, id=equipment_id)
    
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect('lab_detail', lab_id=equipment.laboratory.id)
    else:
        form = EquipmentForm(instance=equipment)

    return render(request, 'inventory/equipment_form.html', {
        'form': form,
        'equipment': equipment,
        'lab': equipment.laboratory,    
        'title': 'Edit Equipment'
    })


@login_required
def equipment_delete(request, equipment_id):
    """Delete equipment."""
    equipment = get_object_or_404(Equipment, id=equipment_id)
    lab_id = equipment.laboratory.id
    if request.method == 'POST':
        equipment.delete()
        return redirect('lab_detail', lab_id=lab_id)

    return render(request, 'inventory/equipment_confirm_delete.html', {
        'equipment': equipment,
        'lab': equipment.laboratory
    })

@login_required
def component_create(request, lab_id):
    """Create new component."""
    lab = get_object_or_404(Laboratory, id=lab_id)
    if request.method == 'POST':
        form = ComponentForm(request.POST)
        if form.is_valid():
            component = form.save(commit=False)
            component.laboratory = lab
            component.save()
            return redirect('lab_detail', lab_id=lab.id)
    else:
        form = ComponentForm()

    return render(request, 'inventory/component_create.html', {
        'form': form,
        'lab': lab,
        'title': 'New Component'
    })

@login_required
def component_update(request, component_id):
    """Update component."""
    component = get_object_or_404(Component, id=component_id)
    
    if request.method == 'POST':
        form = ComponentForm(request.POST, instance=component)
        if form.is_valid():
            form.save()
            return redirect('lab_detail', lab_id=component.laboratory.id)
    else:
        form = ComponentForm(instance=component)

    return render(request, 'inventory/component_update.html', {
        'form': form,
        'component': component,
        'lab': component.laboratory,    
        'title': 'Edit Component'
    })

@login_required
def component_delete(request, component_id):
    """Delete component."""
    component = get_object_or_404(Component, id=component_id)
    lab_id = component.laboratory.id
    if request.method == 'POST':
        component.delete()
        return redirect('lab_detail', lab_id=lab_id)

    return render(request, 'inventory/component_confirm_delete.html', {
        'component': component,
        'lab': component.laboratory
    })

@login_required
def reagent_create(request, lab_id):
    """Create reagent with PubChem auto-fill (MSDS link)."""
    lab = get_object_or_404(Laboratory, id=lab_id)
    message = ""
    form = None

    if request.method == 'POST':
        if 'search_pubchem' in request.POST and request.POST.get('search_pubchem'):
            term = request.POST['search_pubchem'].strip()
            try:
                compounds = pcp.get_compounds(term, 'name')
                if compounds:
                    c = compounds[0]
                    initial_data = {
                        'common_name': term,
                        'iupac_name': c.iupac_name or '',
                        'formula': c.molecular_formula or '',
                        'molecular_weight': float(c.molecular_weight) if c.molecular_weight else None,
                        'pubchem_cid': c.cid,
                    }
                    form = ReagentForm(initial=initial_data)
                    message = f"✅ Data loaded from PubChem (CID: {c.cid}). Review and save."
                else:
                    form = ReagentForm(request.POST)
                    message = "⚠️ No compound found in PubChem."
            except Exception as e:
                form = ReagentForm(request.POST)
                message = f"⚠️ PubChem error: {str(e)}"
        else:
            form = ReagentForm(request.POST)
            if form.is_valid():
                reagent = form.save(commit=False)
                reagent.laboratory = lab
                reagent.save()
                return redirect('lab_detail', lab_id=lab.id)
    else:
        form = ReagentForm()

    return render(request, 'inventory/reagent_form.html', {
        'form': form,
        'lab': lab,
        'message': message
    })


@login_required
def reagent_update(request, reagent_id):
    """Update reagent."""
    reagent = get_object_or_404(Reagent, id=reagent_id)
    if request.method == 'POST':
        form = ReagentForm(request.POST, instance=reagent)
        if form.is_valid():
            form.save()
            return redirect('lab_detail', lab_id=reagent.laboratory.id)
    else:
        form = ReagentForm(instance=reagent)

    return render(request, 'inventory/reagent_form.html', {
        'form': form,
        'reagent': reagent,
        'lab': reagent.laboratory
    })

@login_required
def reagent_delete(request, reagent_id):
    """Delete reagent."""
    reagent = get_object_or_404(Reagent, id=reagent_id)
    lab_id = reagent.laboratory.id
    if request.method == 'POST':
        reagent.delete()
        return redirect('lab_detail', lab_id=lab_id)

    return render(request, 'inventory/reagent_confirm_delete.html', {
        'reagent': reagent,
        'lab': reagent.laboratory
    })

@login_required
def glassware_create(request, lab_id):
    """Create new glassware."""
    lab = get_object_or_404(Laboratory, id=lab_id)
    if request.method == 'POST':
        form = GlasswareForm(request.POST)
        if form.is_valid():
            glassware = form.save(commit=False)
            glassware.laboratory = lab
            glassware.save()
            return redirect('lab_detail', lab_id=lab.id)
    else:
        form = GlasswareForm()

    return render(request, 'inventory/glassware_form.html', {
        'form': form,
        'lab': lab,
        'title': 'New Glassware'
    })


@login_required
def glassware_update(request, glassware_id):
    """Update glassware."""
    glassware = get_object_or_404(Glassware, id=glassware_id)
    if request.method == 'POST':
        form = GlasswareForm(request.POST, instance=glassware)
        if form.is_valid():
            form.save()
            return redirect('lab_detail', lab_id=glassware.laboratory.id)
    else:
        form = GlasswareForm(instance=glassware)

    return render(request, 'inventory/glassware_form.html', {
        'form': form,
        'glassware': glassware,
        'lab': glassware.laboratory,
        'title': 'Edit Glassware'
    })

@login_required
def glassware_delete(request, glassware_id):
    """Delete glassware."""
    glassware = get_object_or_404(Glassware, id=glassware_id)
    lab_id = glassware.laboratory.id
    if request.method == 'POST':
        glassware.delete()
        return redirect('lab_detail', lab_id=lab_id)

    return render(request, 'inventory/glassware_confirm_delete.html', {
        'glassware': glassware,
        'lab': glassware.laboratory
    })


@login_required
def export_lab_to_excel(request, lab_id):
    """Export full laboratory inventory to Excel (Equipment + Reagents)."""
    lab = get_object_or_404(Laboratory, id=lab_id)

    wb = Workbook()
    wb.remove(wb.active)  # eliminar hoja por defecto

    # ====================== EQUIPMENT SHEET ======================
    ws_equip = wb.create_sheet("Equipment")
    headers_equip = ['Name', 'Serial Number', 'Quantity', 'Status', 'Description', 'Notes', 'Updated At']
    
    # Encabezados bonitos
    for col, header in enumerate(headers_equip, 1):
        cell = ws_equip.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="1f4e79", end_color="1f4e79", fill_type="solid")

    equipments = lab.equipments.all().order_by('name')
    for row_idx, eq in enumerate(equipments, 2):
        ws_equip.cell(row=row_idx, column=1, value=eq.name)
        ws_equip.cell(row=row_idx, column=2, value=eq.serial_number)
        ws_equip.cell(row=row_idx, column=3, value=eq.quantity)
        ws_equip.cell(row=row_idx, column=4, value=eq.get_status_display())
        ws_equip.cell(row=row_idx, column=5, value=eq.description or "")
        ws_equip.cell(row=row_idx, column=6, value=eq.notes or "")
        ws_equip.cell(row=row_idx, column=7, value=eq.updated_at.strftime("%Y-%m-%d %H:%M"))

    # Auto-ajustar columnas
    for col in ws_equip.columns:
        max_length = max((len(str(cell.value)) for cell in col if cell.value), default=10)
        ws_equip.column_dimensions[get_column_letter(col[0].column)].width = min(max_length + 2, 50)

    # Título grande
    ws_equip.insert_rows(1)
    title_cell = ws_equip['A1']
    title_cell.value = f"Lab Inventory Report - {lab.name} ({lab.campus.name})"
    title_cell.font = Font(bold=True, size=14)
    ws_equip.merge_cells('A1:G1')

# ====================== GLASSWARE SHEET ======================
    ws_glass = wb.create_sheet("Glassware")
    headers_glass = ['Name', 'Description', 'Volume', 'Quantity', 'Status', 'Notes', 'Updated At']

    # Encabezados bonitos
    for col, header in enumerate(headers_glass, 1):
        cell = ws_glass.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="1f4e79", end_color="1f4e79", fill_type="solid")

    glasswares = lab.glasswares.all().order_by('name')
    for row_idx, gl in enumerate(glasswares, 2):
        ws_glass.cell(row=row_idx, column=1, value=gl.name)
        ws_glass.cell(row=row_idx, column=2, value=gl.description or "")
        ws_glass.cell(row=row_idx, column=3, value=gl.volume)
        ws_glass.cell(row=row_idx, column=4, value=gl.quantity)
        ws_glass.cell(row=row_idx, column=5, value=gl.get_status_display())
        ws_glass.cell(row=row_idx, column=6, value=gl.notes or "")
        ws_glass.cell(row=row_idx, column=7, value=gl.date_updated.strftime("%Y-%m-%d %H:%M"))

    # Auto-ajustar columnas
    for col in ws_glass.columns:
        max_length = max((len(str(cell.value)) for cell in col if cell.value), default=10)
        ws_glass.column_dimensions[get_column_letter(col[0].column)].width = min(max_length + 2, 50)

    # Título grande
    ws_glass.insert_rows(1)
    title_cell = ws_glass['A1']
    title_cell.value = f"Lab Inventory Report - {lab.name} ({lab.campus.name})"
    title_cell.font = Font(bold=True, size=14)
    ws_glass.merge_cells('A1:G1')

# ====================== COMPONENT SHEET ======================
    ws_comp = wb.create_sheet("Components")
    headers_comp = ['Name', 'Description', 'Quantity', 'Status', 'Notes', 'Updated At']

    # Encabezados bonitos
    for col, header in enumerate(headers_comp, 1):
        cell = ws_comp.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="1f4e79", end_color="1f4e79", fill_type="solid")

    components = lab.components.all().order_by('name')
    for row_idx, comp in enumerate(components, 2):
        ws_comp.cell(row=row_idx, column=1, value=comp.name)
        ws_comp.cell(row=row_idx, column=2, value=comp.description or "")
        ws_comp.cell(row=row_idx, column=3, value=comp.quantity)
        ws_comp.cell(row=row_idx, column=4, value=comp.get_status_display())
        ws_comp.cell(row=row_idx, column=5, value=comp.notes or "")
        ws_comp.cell(row=row_idx, column=6, value=comp.date_updated.strftime("%Y-%m-%d %H:%M"))

    # Auto-ajustar columnas
    for col in ws_comp.columns:
        max_length = max((len(str(cell.value)) for cell in col if cell.value), default=10)
        ws_comp.column_dimensions[get_column_letter(col[0].column)].width = min(max_length + 2, 50)

    # Título grande
    ws_comp.insert_rows(1)
    title_cell = ws_comp['A1']
    title_cell.value = f"Lab Inventory Report - {lab.name} ({lab.campus.name})"
    title_cell.font = Font(bold=True, size=14)
    ws_comp.merge_cells('A1:G1')

    # ====================== REAGENTS SHEET ======================
    ws_reag = wb.create_sheet("Reagents")
    headers_reag = ['Common Name', 'Formula', 'Quantity', 'Unit', 'Status', 'CAS Number', 'PubChem CID', 'Safety Notes', 'Updated At']
    
    for col, header in enumerate(headers_reag, 1):
        cell = ws_reag.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="1f4e79", end_color="1f4e79", fill_type="solid")

    reagents = lab.reagents.all().order_by('common_name')
    for row_idx, r in enumerate(reagents, 2):
        ws_reag.cell(row=row_idx, column=1, value=r.common_name)
        ws_reag.cell(row=row_idx, column=2, value=r.formula or "")
        ws_reag.cell(row=row_idx, column=3, value=r.quantity)
        ws_reag.cell(row=row_idx, column=4, value=r.unit)
        ws_reag.cell(row=row_idx, column=5, value=r.get_status_display())
        ws_reag.cell(row=row_idx, column=6, value=r.cas_number or "")
        ws_reag.cell(row=row_idx, column=7, value=r.pubchem_cid or "")
        ws_reag.cell(row=row_idx, column=8, value=r.safety_notes or "")
        ws_reag.cell(row=row_idx, column=9, value=r.updated_at.strftime("%Y-%m-%d %H:%M"))

    # Auto-ajustar
    for col in ws_reag.columns:
        max_length = max((len(str(cell.value)) for cell in col if cell.value), default=10)
        ws_reag.column_dimensions[get_column_letter(col[0].column)].width = min(max_length + 2, 50)

    # Título
    ws_reag.insert_rows(1)
    title_cell = ws_reag['A1']
    title_cell.value = f"Lab Inventory Report - {lab.name} ({lab.campus.name})"
    title_cell.font = Font(bold=True, size=14)
    ws_reag.merge_cells('A1:I1')

    # =================== Respuesta ===================
    filename = f"Lab_Inventory_{lab.name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    wb.save(response)

    return response