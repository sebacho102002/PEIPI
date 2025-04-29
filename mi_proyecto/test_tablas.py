import requests
from bs4 import BeautifulSoup, NavigableString

url = "https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000304786"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

def obtener_formacion_academica():
    for table in soup.find_all("table"):
        h3 = table.find("h3")
        if h3 and "Formación Académica" in h3.get_text(strip=True):
            primera_fila = table.find_all("tr")[1]  # la primera entrada
            celdas = primera_fila.find_all("td")
            if celdas and len(celdas) > 1:
                texto = celdas[1].get_text(separator="\n", strip=True)
                lineas = texto.splitlines()
                if len(lineas) >= 2:
                    nivel = lineas[0]
                    institucion = lineas[1]
                    return f"- Formación académica: {nivel}\n- Institución: {institucion}"
    return "No se encontró formación académica."

def obtener_experiencia_y_cargo():
    for table in soup.find_all("table"):
        h3 = table.find("h3")
        if h3 and "Experiencia profesional" in h3.get_text(strip=True):
            for fila in table.find_all("tr")[1:]:
                celdas = fila.find_all("td")
                if len(celdas) < 2:
                    continue
                contenido = celdas[1]
                if "Actividades de administración" in contenido.get_text():
                    institucion_tag = contenido.find("b")
                    institucion = institucion_tag.get_text(strip=True) if institucion_tag else "No encontrada"

                    for i_tag in contenido.find_all("i"):
                        if "Cargo:" in i_tag.get_text():
                            next_text = i_tag.next_sibling
                            while next_text and (not isinstance(next_text, NavigableString) or not next_text.strip()):
                                next_text = next_text.next_sibling
                            if next_text:
                                bloques = next_text.strip().splitlines()
                                bloques = [b.strip() for b in bloques if b.strip()]
                                cargo = bloques[0] if len(bloques) > 0 else "No encontrado"
                                desde = bloques[1] if len(bloques) > 1 else "Desconocido"
                                hasta = bloques[2] if len(bloques) > 2 else "Actual"
                                return (
                                    f"- Experiencia profesional**: {institucion}\n"
                                    f"- Cargo: {cargo}\n"
                                    f"- Desde: {desde}\n"
                                    f"- Hasta: {hasta}"
                                )

    return "- **Experiencia profesional**: No encontrada\n- **Cargo**: No encontrado"

def listar_tablas_restantes():
    print("\n Otras secciones encontradas:")
    titulos_procesados = [
        "Formación Académica",
        "Experiencia profesional",
    ]
    ya_listadas = set()
    for table in soup.find_all("table"):
        h3 = table.find("h3")
        if not h3:
            continue
        titulo = h3.get_text(strip=True)
        if any(titulo.startswith(t) for t in titulos_procesados):
            continue
        if titulo in ya_listadas:
            continue
        ya_listadas.add(titulo)

        filas_datos = table.find_all("tr")[1:]  # Excluye encabezado
        filas_utiles = [f for f in filas_datos if f.find_all("td")]
        print(f"- {titulo}: {len(filas_utiles)} items")

# Mostrar información principal
print("- Datos procesados:\n")

print(obtener_formacion_academica())
print()
print(obtener_experiencia_y_cargo())

# Mostrar conteo del resto
listar_tablas_restantes()
