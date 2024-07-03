from django import forms
from .models import Entry, ExtractedData

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['name', 'href']

class ExtractedDataForm(forms.ModelForm):
    class Meta:
        model = ExtractedData
        fields = ['entry', 'data']
