import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from scraping.models import Entry, PersonalInfo, Investigacion
from django.db import connection

class Command(BaseCommand):
    help = 'Extract data from the web and store it in the database'

    def handle(self, *args, **kwargs):
        # Limpiar base de datos
        PersonalInfo.objects.all().delete()
        Investigacion.objects.all().delete()
        Entry.objects.all().delete()

        # Reiniciar secuencias de auto-incremento
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='scraping_entry';")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='scraping_personalinfo';")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='scraping_investigacion';")

        url = 'https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000003118'
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find_all('table')[4]  # Tabla donde están los docentes

            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) > 1:
                    name_cell = cells[0]
                    link = name_cell.find('a')
                    if link:
                        name = name_cell.text.strip()
                        href = link.get('href')
                        entry = Entry.objects.create(name=name, href=href)

                        # Extraer información detallada del docente
                        self.extract_docente_data(entry)

        self.stdout.write(self.style.SUCCESS('Data extraction complete'))

    def extract_docente_data(self, entry):
        """Extrae los datos personales e investigaciones de cada docente"""
        response = requests.get(entry.href)
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f"Error accessing URL {entry.href}: {response.status_code}"))
            return

        soup = BeautifulSoup(response.content, 'html.parser')

        try:
            # Extraer información personal
            personal_info_table = soup.find('body').find('div').find_all('table')[1]
            filas_info = personal_info_table.find_all('tr')

            personal_data = {}
            for fila in filas_info:
                columnas = fila.find_all(['th', 'td'])
                if len(columnas) == 2:
                    clave = columnas[0].get_text(strip=True)
                    valor = columnas[1].get_text(strip=True)
                    personal_data[clave] = valor

            # Guardar información personal
            PersonalInfo.objects.create(
                entry=entry,
                nombre=personal_data.get("Nombre", ""),
                identificacion=personal_data.get("Identificación", ""),
                nacionalidad=personal_data.get("Nacionalidad", ""),
                email=personal_data.get("Correo electrónico", ""),
                telefono=personal_data.get("Teléfono", ""),
            )

            # Extraer información de investigaciones
            investigaciones_table = soup.find('body').find('div').find_all('table')[4]
            filas_inv = investigaciones_table.find_all('tr')[1:]  # Omitir encabezado

            for fila in filas_inv:
                columnas = fila.find_all(['th', 'td'])
                if len(columnas) >= 3:
                    titulo = columnas[0].get_text(strip=True)
                    tipo = columnas[1].get_text(strip=True)
                    fecha = columnas[2].get_text(strip=True)
                    institucion = columnas[3].get_text(strip=True) if len(columnas) > 3 else ""

                    Investigacion.objects.create(
                        entry=entry,
                        titulo=titulo,
                        tipo=tipo,
                        fecha=fecha,
                        institucion=institucion
                    )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error processing {entry.href}: {e}"))
