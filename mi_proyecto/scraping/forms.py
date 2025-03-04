from django import forms
from .models import Entry, PersonalInfo, Investigacion

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['name', 'href']

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = ['entry', 'nombre', 'identificacion', 'nacionalidad', 'email', 'telefono']

class InvestigacionForm(forms.ModelForm):
    class Meta:
        model = Investigacion
        fields = ['entry', 'titulo', 'tipo', 'fecha', 'institucion']
