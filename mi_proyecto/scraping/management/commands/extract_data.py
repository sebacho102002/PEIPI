import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from scraping.models import Entry, ExtractedData
import re
from django.db import connection

class Command(BaseCommand):
    help = 'Extract data from the web and store it in the database'

    def handle(self, *args, **kwargs):
        # Borrar todos los datos de la tabla ExtractedData y Entry
        ExtractedData.objects.all().delete()
        Entry.objects.all().delete()

        # Reiniciar el contador de auto-incremento para ExtractedData y Entry
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='scraping_extracteddata';")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='scraping_entry';")

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

                    try:
                        parte_especifica_1 = soup.find('body').find('div').find_all('table')[1]
                        filas_1 = parte_especifica_1.find_all('tr')
                        for fila in filas_1:
                            columnas = fila.find_all(['th', 'td'])
                            fila_datos = [c.get_text(strip=True) for c in columnas]
                            guardar_datos(entry, fila_datos)

                        parte_especifica_4 = soup.find('body').find('div').find_all('table')[4]
                        filas_4 = parte_especifica_4.find_all('tr')
                        if len(filas_4) > 1:
                            segundo_fila = filas_4[1]
                            columnas_4 = segundo_fila.find_all(['th', 'td'])
                            fila_datos_4 = [c.get_text(strip=True) for c in columnas_4]
                            guardar_datos(entry, fila_datos_4)
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error processing URL {url}: {e}"))
                else:
                    self.stdout.write(self.style.ERROR(f"Error accessing URL {url}: {response.status_code}"))

        self.stdout.write(self.style.SUCCESS('Data extraction complete'))

        # Imprimir los datos estructurados en consola
        self.stdout.write("\nDatos extraídos:")
        for entry in Entry.objects.all():
            self.stdout.write(f"\n=== {entry.name} ===")
            for dato in ExtractedData.objects.filter(entry=entry):
                clave, valor = parsear_dato(dato.data)
                if valor:
                    self.stdout.write(f"{clave}: {valor}")
                else:
                    self.stdout.write(f"{clave}")


def guardar_datos(entry, fila_datos):
    """Procesa y guarda los datos en la base de datos."""
    fila_limpiada = limpiar_datos(fila_datos)
    for dato in fila_limpiada:
        if dato:  # Guardar solo si el dato no está vacío
            ExtractedData.objects.create(entry=entry, data=dato)


def parsear_dato(dato):
    """Divide un dato en clave y valor para mostrarlo de forma estructurada."""
    if ':' in dato:
        clave, valor = dato.split(':', 1)
        return clave.strip(), valor.strip()
    return dato.strip(), None


def extraer_letras(texto):
    """Extrae solo letras incluyendo tildes y la letra Ñ."""
    letras = re.findall(r'[a-zA-ZáéíóúüÁÉÍÓÚÜñÑ]+', texto)
    return ' '.join(letras)


def limpiar_datos(datos):
    """Limpia y estructura los datos."""
    datos_limpios = []
    for dato in datos:
        if ':' in dato:
            clave, valor = dato.split(':', 1)
            clave = clave.strip()
            valor = valor.strip()
            valor = corregir_formato_texto(valor)
            datos_limpios.append(f"{extraer_letras(clave)}: {extraer_letras(valor)}")
        else:
            dato_limpio = corregir_formato_texto(dato)
            letras_extraidas = extraer_letras(dato_limpio)
            if letras_extraidas:  # Añadir solo si no está vacío
                datos_limpios.append(letras_extraidas)
    return datos_limpios


def corregir_formato_texto(texto):
    """Divide palabras unidas y realiza ajustes de formato."""
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
