from django.shortcuts import render, get_object_or_404, redirect
from .models import Entry, PersonalInfo, Investigacion
from .forms import EntryForm
from django.http import JsonResponse
import json
import os

# 📌 Página de inicio
def home_page(request):
    return render(request, 'home.html')

# 📌 Base
def base(request):
    entry = "Some entry data"
    return render(request, 'base.html', {'entry': entry})

# 📌 Vista de Ingeniería de Sistemas
def ingenieria_sistemas_view(request):
    json_file_path = os.path.join(os.path.dirname(__file__), '..', 'data.json')

    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = []  # Si no hay datos, se devuelve una lista vacía

    return render(request, 'ingenieria_sistemas.html', {'data': data})

# 📌 Lista de todas las entradas
def entry_list(request):
    entries = Entry.objects.all()
    return render(request, 'scraping/entry_list.html', {'entries': entries})

# 📌 Vista detallada de un docente con tabla de investigaciones mejorada
def entry_detail(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    
    # Obtener información personal e investigaciones del docente
    personal_info = PersonalInfo.objects.filter(entry=entry).first()
    investigaciones = Investigacion.objects.filter(entry=entry).order_by('id')  # Se asegura el orden en que se obtuvieron

    return render(request, 'scraping/entry_detail.html', {
        'entry': entry,
        'personal_info': personal_info,
        'investigaciones': investigaciones
    })

# 📌 Crear una nueva entrada
def entry_new(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save()
            return redirect('entry_detail', pk=entry.pk)
    else:
        form = EntryForm()
    return render(request, 'scraping/entry_edit.html', {'form': form})

# 📌 Editar una entrada
def entry_edit(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if request.method == "POST":
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            entry = form.save()
            return redirect('entry_detail', pk=entry.pk)
    else:
        form = EntryForm(instance=entry)
    return render(request, 'scraping/entry_edit.html', {'form': form})

# 📌 Eliminar una entrada
def entry_delete(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    entry.delete()
    return redirect('entry_list')

# 📌 Generar JSON con los datos de los docentes
def extracted_data_list(request):
    entries = Entry.objects.all()
    data = []

    for entry in entries:
        personal_info = PersonalInfo.objects.filter(entry=entry).first()
        investigaciones = Investigacion.objects.filter(entry=entry).order_by('id')  # Ordenadas por ID

        data.append({
            'name': entry.name,
            'href': entry.href,
            'personal_info': {
                'nombre': personal_info.nombre if personal_info else None,
                'nombre_citaciones': personal_info.nombre_citaciones if personal_info else None,
                'categoria': personal_info.categoria if personal_info else None,
                'par_evaluador': personal_info.par_evaluador if personal_info else None,
                'nacionalidad': personal_info.nacionalidad if personal_info else None,
                'sexo': personal_info.sexo if personal_info else None,
            } if personal_info else None,
            'investigaciones': [
                {
                    'titulo': inv.titulo,
                    'tipo': inv.tipo,
                    'fecha': inv.fecha,
                    'institucion': inv.institucion
                } for inv in investigaciones
            ]
        })

    return JsonResponse(data, safe=False)
