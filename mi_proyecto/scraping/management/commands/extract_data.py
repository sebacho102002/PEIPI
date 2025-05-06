import requests
from bs4 import BeautifulSoup, NavigableString
from django.core.management.base import BaseCommand
from scraping.models import (
    Entry,
    PersonalInfo,
    Investigacion,
    FormacionAcademica,
    ExperienciaProfesional,
)

GRUPLAC_URL = "https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000003118"

class Command(BaseCommand):
    help = 'Extrae datos de Gruplac y CvLAC y los almacena en la base de datos'

    def handle(self, *args, **kwargs):
        self.stdout.write("🟢 Iniciando extracción de datos...\n")

        # Limpieza completa
        Investigacion.objects.all().delete()
        FormacionAcademica.objects.all().delete()
        ExperienciaProfesional.objects.all().delete()
        PersonalInfo.objects.all().delete()
        Entry.objects.all().delete()

        docentes = self.obtener_docentes()
        if not docentes:
            self.stdout.write("⚠️ No se encontraron docentes.")
            return

        for nombre, perfil_url in docentes:
            self.stdout.write(f"\n🔎 Procesando: {nombre}")
            entry, _ = Entry.objects.get_or_create(name=nombre, href=perfil_url)

            response = requests.get(perfil_url)
            if response.status_code != 200:
                self.stdout.write(f"⚠️ No se pudo acceder al perfil de {entry.name}.")
                continue

            soup = BeautifulSoup(response.content, "html.parser")

            info_personal = self.obtener_info_personal(soup, entry)
            if info_personal:
                PersonalInfo.objects.update_or_create(entry=entry, defaults=info_personal)

            if self.obtener_formacion_academica(soup, entry):
                self.stdout.write("📘 Formación académica registrada.")

            if self.obtener_experiencia_y_cargo(soup, entry):
                self.stdout.write("🧳 Experiencia profesional registrada.")

            self.obtener_investigaciones_agrupadas(soup, entry)

        self.stdout.write("\n✅ Extracción y almacenamiento completados exitosamente.")

    def obtener_docentes(self):
        response = requests.get(GRUPLAC_URL)
        if response.status_code != 200:
            self.stdout.write(f"🔴 Error al acceder a GRUPLAC: {response.status_code}")
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        tables = soup.find_all("table")
        if len(tables) < 5:
            self.stdout.write("⚠️ No hay suficientes tablas.")
            return []

        docentes = []
        for row in tables[4].find_all("tr")[1:]:
            cols = row.find_all("td")
            if cols:
                name = cols[0].get_text(strip=True)
                link = cols[0].find("a")
                href = link.get("href") if link else None
                if href:
                    full_url = href if href.startswith("http") else f"https://scienti.minciencias.gov.co{href}"
                    docentes.append((name, full_url))
        return docentes

    def obtener_info_personal(self, soup, entry):
        info_personal = {
            "nombre": entry.name,
            "nombre_citaciones": "",
            "categoria": "",
            "par_evaluador": False,
            "nacionalidad": "",
            "sexo": "",
        }

        for table in soup.find_all("table"):
            for row in table.find_all("tr"):
                cols = row.find_all("td")
                if len(cols) >= 2:
                    clave = cols[0].get_text(strip=True).lower()
                    valor = cols[1].get_text(strip=True)

                    if "categoría" in clave and not info_personal["categoria"]:
                        info_personal["categoria"] = valor
                    elif "par evaluador" in clave:
                        info_personal["par_evaluador"] = True
                    elif "nombre en citaciones" in clave:
                        info_personal["nombre_citaciones"] = valor
                    elif "nacionalidad" in clave:
                        info_personal["nacionalidad"] = valor
                    elif "sexo" in clave:
                        info_personal["sexo"] = valor

        return info_personal

    def obtener_formacion_academica(self, soup, entry):
        for table in soup.find_all("table"):
            h3 = table.find("h3")
            if h3 and "Formación Académica" in h3.get_text(strip=True):
                rows = table.find_all("tr")
                if len(rows) > 1:
                    cols = rows[1].find_all("td")
                    if len(cols) > 1:
                        texto = cols[1].get_text(separator="\n", strip=True)
                        lineas = texto.splitlines()
                        if len(lineas) >= 2:
                            nivel, institucion = lineas[0], lineas[1]
                            FormacionAcademica.objects.update_or_create(
                                entry=entry,
                                defaults={"nivel": nivel, "institucion": institucion}
                            )
                            return True
        return False

    def obtener_experiencia_y_cargo(self, soup, entry):
        for table in soup.find_all("table"):
            h3 = table.find("h3")
            if h3 and "Experiencia profesional" in h3.get_text(strip=True):
                for row in table.find_all("tr")[1:]:
                    cols = row.find_all("td")
                    if len(cols) < 2:
                        continue
                    contenido = cols[1]
                    if "Actividades de administración" in contenido.get_text():
                        institucion_tag = contenido.find("b")
                        institucion = institucion_tag.get_text(strip=True) if institucion_tag else "Desconocida"

                        for i_tag in contenido.find_all("i"):
                            if "Cargo:" in i_tag.get_text():
                                next_text = i_tag.next_sibling
                                while next_text and (not isinstance(next_text, NavigableString) or not next_text.strip()):
                                    next_text = next_text.next_sibling
                                if next_text:
                                    bloques = next_text.strip().splitlines()
                                    bloques = [b.strip() for b in bloques if b.strip()]
                                    cargo = bloques[0] if len(bloques) > 0 else "Desconocido"
                                    desde = bloques[1] if len(bloques) > 1 else ""
                                    hasta = bloques[2] if len(bloques) > 2 else ""
                                    ExperienciaProfesional.objects.update_or_create(
                                        entry=entry,
                                        defaults={
                                            "institucion": institucion,
                                            "cargo": cargo,
                                            "desde": desde,
                                            "hasta": hasta
                                        }
                                    )
                                    return True
        return False

    def obtener_investigaciones_agrupadas(self, soup, entry):
        procesadas = {"Formación Académica", "Experiencia profesional"}
        datos_investigacion = {}

        for table in soup.find_all("table"):
            h3 = table.find("h3")
            if not h3:
                continue

            titulo = h3.get_text(strip=True)
            if titulo in procesadas or titulo in datos_investigacion:
                continue

            filas = table.find_all("tr")[1:]
            filas_utiles = [f for f in filas if f.find_all("td")]

            if filas_utiles:
                datos_investigacion[titulo] = len(filas_utiles)

        if datos_investigacion:
            Investigacion.objects.update_or_create(
                entry=entry,
                defaults={'datos': datos_investigacion}
            )
