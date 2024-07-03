import requests
from bs4 import BeautifulSoup
import json
from django.core.management.base import BaseCommand
from scraping.models import Entry, ExtractedData

class Command(BaseCommand):
    help = 'Extract data from the web and store it in the database'

    def handle(self, *args, **kwargs):
        url = 'https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000003118'
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find_all('table')[4]
            data = []

            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) > 1:
                    name_cell = cells[0]
                    link = name_cell.find('a')
                    if link:
                        name = name_cell.text.strip()
                        href = link.get('href')
                        entry = Entry.objects.create(name=name, href=href)
                        data.append(entry)

            for entry in Entry.objects.all():
                url = entry.href
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    datos_ordenados = []

                    try:
                        parte_especifica_1 = soup.find('body').find('div').find_all('table')[1]
                        filas_1 = parte_especifica_1.find_all('tr')
                        for fila in filas_1:
                            columnas = fila.find_all(['th', 'td'])
                            fila_datos = [c.get_text(strip=True) for c in columnas]
                            fila_limpiada = limpiar_datos(fila_datos)
                            datos_ordenados.append(fila_limpiada)

                        parte_especifica_4 = soup.find('body').find('div').find_all('table')[4]
                        filas_4 = parte_especifica_4.find_all('tr')
                        if len(filas_4) > 1:
                            segundo_fila = filas_4[1]
                            columnas_4 = segundo_fila.find_all(['th', 'td'])
                            fila_datos_4 = [c.get_text(strip=True) for c in columnas_4]
                            fila_limpiada_4 = limpiar_datos(fila_datos_4)
                            datos_ordenados.append(fila_limpiada_4)

                        ExtractedData.objects.create(entry=entry, data=datos_ordenados)
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error processing URL {url}: {e}"))
                else:
                    self.stdout.write(self.style.ERROR(f"Error accessing URL {url}: {response.status_code}"))

        self.stdout.write(self.style.SUCCESS('Data extraction complete'))

def limpiar_datos(datos):
    datos_limpios = []
    for dato in datos:
        if ':' in dato:
            clave, valor = dato.split(':', 1)
            clave = clave.strip()
            valor = valor.strip()
            valor = corregir_formato_texto(valor)
            datos_limpios.append([clave, valor])
        else:
            dato_limpio = corregir_formato_texto(dato)
            datos_limpios.append(['', dato_limpio])
    return datos_limpios

def corregir_formato_texto(texto):
    # Dividir palabras unidas en mayúsculas y otros ajustes de formato
    palabras = []
    palabra_actual = ''
    for caracter in texto:
        if caracter.isupper() and palabra_actual and not palabra_actual[-1].isspace():
            palabras.append(palabra_actual)
            palabra_actual = caracter
        else:
            palabra_actual += caracter
    if palabra_actual:
        palabras.append(palabra_actual)
    return ' '.join(palabras)
