from django import forms
from .models import Component, Equipment, Reagent, Glassware

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'description', 'serial_number', 'quantity', 'status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class ReagentForm(forms.ModelForm):
    search_pubchem = forms.CharField(
        required=False,
        label="Search PubChem (name or CAS)",
        help_text="Example: 'hydrochloric acid' or '7647-01-0'"
    )

    class Meta:
        model = Reagent
        fields = ['common_name', 'formula', 'molecular_weight', 'cas_number', 'pubchem_cid' , 'quantity', 'unit', 'status', 'safety_notes']
        widgets = {
            'safety_notes': forms.Textarea(attrs={'rows': 3}),
        }

class GlasswareForm(forms.ModelForm):
    class Meta:
        model = Glassware
        fields = ['name', 'description', 'volume', 'quantity', 'status', 'status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ['name', 'description', 'quantity', 'status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }