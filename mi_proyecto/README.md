# PEIPI - Plataforma para la Extracción de Informes de Profesores e Investigadores

**Proyecto desarrollado en Django para automatizar la extracción de información académica de docentes desde CvLAC y exportarla en formato Excel de manera personalizada.**

---

## Tabla de Contenidos
- [Descripción General](#descripción-general)
- [Tecnologías Usadas](#tecnologías-usadas)
- [Requerimientos](#requerimientos)
- [Instalación](#instalación)
- [Ejecución del Proyecto](#ejecución-del-proyecto)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Funcionalidades Implementadas](#funcionalidades-implementadas)
- [Scraping](#scraping)
- [Exportación de Datos](#exportación-de-datos)
- [Vistas y Frontend](#vistas-y-frontend)
- [Consideraciones Especiales](#consideraciones-especiales)
- [Notas Adicionales](#notas-adicionales)

---

## Descripción General

PEIPI permite:
- Automatizar la recolección de datos académicos de docentes desde CvLAC (proyectos, artículos, libros, formación, experiencia, etc.).
- Normalizar los nombres para que se vean correctamente (evitando números, símbolos, etc.).
- Exportar los datos a un archivo Excel **personalizado** según las necesidades del usuario.
- Ejecutar el scraping desde una vista web con una **barra de progreso animada** y una consola visual de seguimiento.
- Usar Bootstrap 5 para tener una interfaz moderna y responsiva.

---

## Tecnologías Usadas
- **Python 3.13**
- **Django 5.1**
- **SQLite** como base de datos (por defecto).
- **Bootstrap 5** (para la interfaz de usuario).
- **BeautifulSoup 4** (para el scraping).
- **OpenPyXL** (para generar archivos `.xlsx`).

---

## Requerimientos

- Python 3.8 o superior.
- Django 5.0 o superior.
- Librerías:
  - `beautifulsoup4`
  - `openpyxl`
  - `requests`

Instalación de dependencias:

```bash
pip install -r requirements.txt
Instalación
Clona el repositorio:

bash
Copiar
Editar
git clone https://github.com/tu_usuario/peipi.git
cd peipi
Crea un entorno virtual:

bash
Copiar
Editar
python3 -m venv venv
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate.bat # En Windows
Instala las dependencias:

bash
Copiar
Editar
pip install -r requirements.txt
Realiza las migraciones de base de datos:

bash
Copiar
Editar
python manage.py migrate
Crea un superusuario para el Django Admin:

bash
Copiar
Editar
python manage.py createsuperuser
Corre el servidor:

bash
Copiar
Editar
python manage.py runserver
Ejecución del Proyecto
Ingresa a http://127.0.0.1:8000/.

Usa la opción "Exportar Datos" para:

Ejecutar scraping.

Visualizar progreso.

Exportar los datos extraídos a Excel personalizado.

Estructura del Proyecto
bash
Copiar
Editar
mi_proyecto/
│
├── scraping/
│   ├── migrations/
│   ├── management/commands/extract_data.py  # Script de Scraping
│   ├── templates/
│   │   ├── scraping/
│   │   │   ├── entry_list.html
│   │   │   ├── entry_detail.html
│   │   │   ├── exportar_datos.html
│   ├── static/
│   │   └── img/LogoUSC.png
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│
├── manage.py
├── requirements.txt
└── README.md
Funcionalidades Implementadas
✅ Limpieza de datos antes de cada scraping (borrado seguro y reset de IDs).
✅ Extracción de docentes desde GRUPLAC.
✅ Normalización de nombres extraídos (evita números y símbolos raros).
✅ Eliminación de secciones no relevantes como "Hoja de Vida".
✅ Generación de Excel dinámico:

Permite elegir qué datos incluir.

Permite elegir la estructura del archivo (una hoja, una hoja por docente, una hoja por tipo de datos).
✅ Barra de progreso visual y consola de mensajes en tiempo real.
✅ Prevención de cierre accidental mientras se ejecuta scraping.
✅ Vistas limpias usando Bootstrap 5.

Scraping
El scraping se ejecuta con python manage.py extract_data o desde la opción web de "Ejecutar Scraping".

Los datos extraídos incluyen:

Información personal (nombre, nacionalidad, género, etc.).

Formación académica.

Experiencia profesional.

Número de investigaciones agrupadas por sección (proyectos, artículos, libros, etc.).

Exportación de Datos
Desde la sección Exportar Datos puedes:

Seleccionar:

Información personal.

Formación académica.

Experiencia profesional.

Investigaciones.

Elegir el tipo de exportación:

Todo en una hoja.

Cada docente en una hoja.

Cada tipo de dato en una hoja.

El archivo se descarga automáticamente como:

Copiar
Editar
docentes_exportados_YYYYMMDD_HHMMSS.xlsx
Vistas y Frontend
entry_list.html: Lista de docentes con barra de búsqueda interactiva.

entry_detail.html: Vista detallada de cada docente.

exportar_datos.html: Exportación y scraping con barra de progreso + consola en tiempo real.

entry_edit.html: Edición elegante de docentes y datos asociados.

Todas las páginas están adaptadas a Bootstrap 5 y son totalmente responsivas.

Consideraciones Especiales
El scraping es seguro y no genera duplicados.

Cada vez que se ejecuta scraping:

Se eliminan los registros anteriores.

Se reinicia el contador de ID de docentes (Entry) para mantener orden.

El scraping limpia automáticamente nombres, eliminando caracteres raros.

Si se intenta cerrar la página durante scraping, aparece una advertencia.

Notas Adicionales
Proyecto diseñado para crecimiento futuro: se pueden agregar filtros por facultades, líneas de investigación, etc.

Soporta agregar campos adicionales de exportación si es necesario (por ejemplo: idiomas, reconocimientos).

El modelo de Investigaciones usa JSONField para almacenar los conteos de cada sección.

Se planea en el futuro incorporar exportación a PDF tipo informe profesional.

¡Gracias por revisar este proyecto! 

