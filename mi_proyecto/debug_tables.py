import requests
from bs4 import BeautifulSoup

# URL de la página principal del grupo
GRUPLAC_URL = "https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000003118"

def analizar_tablas(url):
    """Obtiene y analiza las tablas de la página especificada."""
    response = requests.get(url)

    if response.status_code != 200:
        print(f"🔴 Error al acceder a la URL: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup.find_all("table")

    print(f"✅ Número de tablas encontradas: {len(tables)}\n")

    for i, table in enumerate(tables[:5]):  # Solo mostramos las primeras 5 tablas
        print(f"📌 Tabla {i}:")
        rows = table.find_all("tr")[:3]  # Solo mostramos las primeras 3 filas

        for row in rows:
            columns = row.find_all(["th", "td"])
            row_text = [col.get_text(strip=True) for col in columns]
            print(row_text)

        print("\n" + "="*80 + "\n")

def obtener_docentes():
    """Extrae la lista de docentes del grupo y sus enlaces de perfil."""
    response = requests.get(GRUPLAC_URL)

    if response.status_code != 200:
        print(f"🔴 Error al acceder a la URL del grupo: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup.find_all("table")

    if len(tables) < 5:
        print("⚠️ No hay suficientes tablas en la página. Verifica la URL.")
        return []

    # La tabla 4 suele contener la información de los docentes
    docentes_tabla = tables[4]
    docentes = []

    for row in docentes_tabla.find_all("tr")[1:]:  # Omitimos la cabecera
        columns = row.find_all("td")
        if len(columns) > 0:
            name = columns[0].get_text(strip=True)
            link = columns[0].find("a")
            href = link.get("href") if link else None

            if href:
                # ✅ Corrección en la construcción de la URL del perfil del docente
                full_url = href if href.startswith("http") else f"https://scienti.minciencias.gov.co{href}"
                docentes.append((name, full_url))

    return docentes

if __name__ == "__main__":
    print("🟢 1️⃣ Analizando la página principal de Gruplac...\n")
    print(f"🔍 Analizando {GRUPLAC_URL}")
    analizar_tablas(GRUPLAC_URL)

    print("\n🟢 2️⃣ Extrayendo docentes y accediendo a sus perfiles...\n")
    docentes = obtener_docentes()

    if not docentes:
        print("⚠️ No se encontraron docentes en la tabla 4.")
    else:
        for i, (nombre, perfil_url) in enumerate(docentes[:3]):  # Solo analizamos 3 docentes
            print(f"\n🔎 Analizando perfil del docente {i+1}: {nombre}")
            print(f"🌐 URL: {perfil_url}\n")
            analizar_tablas(perfil_url)
