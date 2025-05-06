from django.contrib import admin
from .models import Entry, PersonalInfo, Investigacion, FormacionAcademica, ExperienciaProfesional

admin.site.register(Entry)
admin.site.register(PersonalInfo)
admin.site.register(Investigacion)
admin.site.register(FormacionAcademica)
admin.site.register(ExperienciaProfesional)
