from django import forms
from .models import Entry, PersonalInfo, Investigacion

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['name', 'href']

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = [
            'entry',
            'nombre',
            'nombre_citaciones',
            'categoria',
            'par_evaluador',
            'nacionalidad',
            'sexo'
        ]

class InvestigacionForm(forms.ModelForm):
    class Meta:
        model = Investigacion
        fields = ['entry', 'datos']
