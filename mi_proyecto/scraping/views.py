from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Entry, ExtractedData
from .forms import EntryForm, ExtractedDataForm # type: ignore
from django.http import JsonResponse
from .models import ExtractedData
import json




def home_page(request):
    return render(request, 'home.html')

def base(request):
    entry = "Some entry data"  # Asegúrate de definir 'entry' con algún valor
    return render(request, 'base.html', {'entry': entry})

def ingenieria_sistemas_view(request):
    import os
    import json
    
    # Obtener la ruta completa al archivo data.json
    json_file_path = os.path.join(os.path.dirname(__file__), '..', 'data.json')

    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = []  # Manejar el caso en el que el archivo no exista

    return render(request, 'ingenieria_sistemas.html', {'data': data})

def detail_page(request, pk):
    entry = Entry.objects.get(pk=pk)
    return render(request, 'detail.html', {'entry': entry})

def entry_list(request):
    entries = Entry.objects.all()
    return render(request, 'scraping/entry_list.html', {'entries': entries})

def entry_detail(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    return render(request, 'scraping/entry_detail.html', {'entry': entry})

def entry_new(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save()
            return redirect('entry_detail', pk=entry.pk)
    else:
        form = EntryForm()
    return render(request, 'scraping/entry_edit.html', {'form': form})

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

def entry_delete(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    entry.delete()
    return redirect('entry_list')

def extracted_data_list(request):
    extracted_data = ExtractedData.objects.all()
    data = []
    for item in extracted_data:
        data.append({
            'name': item.entry.name,
            'href': item.entry.href,
            'data': item.data,
        })
    return JsonResponse(data, safe=False)