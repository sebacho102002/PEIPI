from django.db import models

class Entry(models.Model):
    name = models.CharField(max_length=255)
    href = models.URLField()

class PersonalInfo(models.Model):
    entry = models.OneToOneField(Entry, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    identificacion = models.CharField(max_length=100, blank=True, null=True)
    nacionalidad = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)

class Investigacion(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.CharField(max_length=50, blank=True, null=True)
    institucion = models.CharField(max_length=255, blank=True, null=True)
