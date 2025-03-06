from django.db import models

class Entry(models.Model):
    name = models.CharField(max_length=255)
    href = models.URLField()

    def __str__(self):
        return self.name

class PersonalInfo(models.Model):
    entry = models.OneToOneField(Entry, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    nombre_citaciones = models.CharField(max_length=255, blank=True, null=True)  # Nuevo campo
    categoria = models.CharField(max_length=255, blank=True, null=True)  # Nuevo campo
    par_evaluador = models.BooleanField(default=False)  # Nuevo campo
    nacionalidad = models.CharField(max_length=100, blank=True, null=True)
    sexo = models.CharField(max_length=50, blank=True, null=True)  # Nuevo campo

    def __str__(self):
        return f"{self.nombre} - {self.entry.name}"

class Investigacion(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=500)
    tipo = models.CharField(max_length=255, blank=True, null=True)
    fecha = models.CharField(max_length=100, blank=True, null=True)
    institucion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.titulo
