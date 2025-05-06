from django.shortcuts import render, get_object_or_404, redirect
from .models import Entry, PersonalInfo, Investigacion, FormacionAcademica, ExperienciaProfesional
from .forms import EntryForm
from django.http import JsonResponse
import json
import os
from django.http import HttpResponse
from openpyxl import Workbook
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.management import call_command

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
        data = []
    return render(request, 'ingenieria_sistemas.html', {'data': data})

def entry_list(request):
    query = request.GET.get("q")
    entries = Entry.objects.filter(name__icontains=query) if query else Entry.objects.all()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('scraping/_entry_list_items.html', {'entries': entries})
        return JsonResponse({'html': html})

    return render(request, 'scraping/entry_list.html', {'entries': entries})


# 📌 Vista detallada de un docente
def entry_detail(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    personal_info = PersonalInfo.objects.filter(entry=entry).first()
    formacion = FormacionAcademica.objects.filter(entry=entry).first()
    experiencia = ExperienciaProfesional.objects.filter(entry=entry).first()
    investigaciones = Investigacion.objects.filter(entry=entry).first()

    return render(request, 'scraping/entry_detail.html', {
        'entry': entry,
        'personal_info': personal_info,
        'formacion': formacion,
        'experiencia': experiencia,
        'investigaciones': investigaciones,
    })

# 📌 Crear nueva entrada
def entry_new(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save()
            return redirect('entry_detail', pk=entry.pk)
    else:
        form = EntryForm()
    return render(request, 'scraping/entry_edit.html', {'form': form})

# 📌 Editar entrada existente
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

# 📌 Exportar JSON de los docentes
def extracted_data_list(request):
    entries = Entry.objects.all()
    data = []

    for entry in entries:
        personal_info = PersonalInfo.objects.filter(entry=entry).first()
        investigacion = Investigacion.objects.filter(entry=entry).first()

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
            'investigaciones': investigacion.datos if investigacion and investigacion.datos else {}
        })

    return JsonResponse(data, safe=False)

@csrf_exempt
def exportar_datos_view(request):
    if request.method == 'POST':
        seleccion = request.POST.getlist('opciones')
        wb = Workbook()
        ws = wb.active
        ws.title = "Datos Exportados"

        # Encabezados dinámicos
        headers = []
        if 'personal_info' in seleccion:
            headers.extend(['Nombre', 'Nombre en Citaciones', 'Categoría', 'Par Evaluador', 'Nacionalidad', 'Sexo'])
        if 'formacion' in seleccion:
            headers.extend(['Nivel Académico', 'Institución Académica'])
        if 'experiencia' in seleccion:
            headers.extend(['Institución Laboral', 'Cargo', 'Desde', 'Hasta'])
        if 'investigacion' in seleccion:
            headers.extend(['Sección', 'Total de Ítems'])

        ws.append(headers)

        for entry in Entry.objects.all():
            fila = []
            if 'personal_info' in seleccion:
                pi = getattr(entry, 'personal_info', None)
                fila.extend([
                    pi.nombre if pi else '',
                    pi.nombre_citaciones if pi else '',
                    pi.categoria if pi else '',
                    'Sí' if pi and pi.par_evaluador else 'No',
                    pi.nacionalidad if pi else '',
                    pi.sexo if pi else '',
                ])
            if 'formacion' in seleccion:
                fa = getattr(entry, 'formacion_academica', None)
                fila.extend([
                    fa.nivel if fa else '',
                    fa.institucion if fa else '',
                ])
            if 'experiencia' in seleccion:
                ep = getattr(entry, 'experiencia_profesional', None)
                fila.extend([
                    ep.institucion if ep else '',
                    ep.cargo if ep else '',
                    ep.desde if ep else '',
                    ep.hasta if ep else '',
                ])
            if 'investigacion' in seleccion:
                inv = getattr(entry, 'investigaciones', None)
                if inv and inv.datos:
                    for seccion, cantidad in inv.datos.items():
                        fila.extend([seccion, cantidad])
                else:
                    fila.extend(['', ''])
            ws.append(fila)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=datos_exportados.xlsx'
        wb.save(response)
        return response

    return render(request, 'scraping/exportar_datos.html')

def ejecutar_scraping(request):
    try:
        call_command('extract_data')
        return JsonResponse({'mensaje': 'Scraping ejecutado exitosamente.'})
    except Exception as e:
        return JsonResponse({'mensaje': f'Error durante el scraping: {str(e)}'}, status=500)