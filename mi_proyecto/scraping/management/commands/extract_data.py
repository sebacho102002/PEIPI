import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from scraping.models import Entry, PersonalInfo, Investigacion
import re

# URL del listado de docentes en Gruplac
GRUPLAC_URL = "https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000003118"

class Command(BaseCommand):
    help = 'Extrae datos de Gruplac y los almacena en la base de datos'

    def handle(self, *args, **kwargs):
        self.stdout.write("🟢 Iniciando extracción de datos...\n")

        # 🔹 Limpiar la base de datos antes de insertar nuevos datos
        Entry.objects.all().delete()
        PersonalInfo.objects.all().delete()
        Investigacion.objects.all().delete()

        # 🔹 Obtener lista de docentes
        docentes = self.obtener_docentes()

        if not docentes:
            self.stdout.write("⚠️ No se encontraron docentes en la tabla 4.")
            return

        # 🔹 Procesar cada docente
        for nombre, perfil_url in docentes:
            self.stdout.write(f"\n🔎 Procesando: {nombre}")
            entry = Entry.objects.create(name=nombre, href=perfil_url)

            # 🔹 Extraer y almacenar información personal del docente
            info_personal = self.obtener_info_personal(perfil_url, entry)
            if info_personal:
                PersonalInfo.objects.create(entry=entry, **info_personal)

            # 🔹 Extraer y almacenar investigaciones
            investigaciones = self.obtener_investigaciones(perfil_url, entry)
            for inv in investigaciones:
                Investigacion.objects.create(entry=entry, **inv)

        self.stdout.write("\n✅ Extracción y almacenamiento completados exitosamente.")

    def obtener_docentes(self):
        """Extrae la lista de docentes del grupo y sus enlaces de perfil."""
        response = requests.get(GRUPLAC_URL)
        if response.status_code != 200:
            self.stdout.write(f"🔴 Error al acceder a la URL del grupo: {response.status_code}")
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        tables = soup.find_all("table")

        if len(tables) < 5:
            self.stdout.write("⚠️ No hay suficientes tablas en la página. Verifica la URL.")
            return []

        # 📌 La tabla 4 contiene la información de los docentes
        docentes_tabla = tables[4]
        docentes = []

        for row in docentes_tabla.find_all("tr")[1:]:  # Omitimos la cabecera
            columns = row.find_all("td")
            if len(columns) > 0:
                name = columns[0].get_text(strip=True)
                link = columns[0].find("a")
                href = link.get("href") if link else None

                if href:
                    full_url = href if href.startswith("http") else f"https://scienti.minciencias.gov.co{href}"
                    docentes.append((name, full_url))

        return docentes

    def obtener_info_personal(self, url, entry):
        """Extrae información personal del docente desde su perfil."""
        response = requests.get(url)
        if response.status_code != 200:
            self.stdout.write(f"⚠️ No se pudo acceder al perfil de {entry.name}.")
            return None

        soup = BeautifulSoup(response.content, "html.parser")
        tables = soup.find_all("table")

        if len(tables) < 1:
            self.stdout.write(f"⚠️ No hay tablas suficientes en el perfil de {entry.name}.")
            return None

        # 📌 La tabla 0 usualmente contiene los datos personales
        datos = tables[0].find_all("td")

        info_personal = {
            "nombre": self.extraer_texto(datos, 5),
            "nombre_citaciones": self.extraer_texto(datos, 7),
            "categoria": self.extraer_texto(datos, 3),
            "par_evaluador": "Par evaluador" in self.extraer_texto(datos, 1),
            "nacionalidad": self.extraer_texto(datos, 9),
            "sexo": self.extraer_texto(datos, 11),
        }

        return info_personal

    def obtener_investigaciones(self, url, entry):
        """Extrae la lista de investigaciones del docente."""
        response = requests.get(url)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        tables = soup.find_all("table")

        if len(tables) < 5:
            return []

        investigaciones = []
        tabla_investigaciones = tables[4]  # 📌 La tabla 4 contiene las investigaciones

        for row in tabla_investigaciones.find_all("tr")[1:]:  # Omitimos la cabecera
            columns = row.find_all("td")
            if len(columns) >= 4:
                inv = {
                    "titulo": columns[0].get_text(strip=True),
                    "tipo": columns[1].get_text(strip=True),
                    "fecha": columns[2].get_text(strip=True),
                    "institucion": columns[3].get_text(strip=True),
                }
                investigaciones.append(inv)

        return investigaciones

    def extraer_texto(self, elementos, indice):
        """Extrae texto de un índice específico en una lista de elementos."""
        return elementos[indice].get_text(strip=True) if len(elementos) > indice else ""
