from django.db import models

class Entry(models.Model):
    """
    Modelo que representa un docente con información básica y su enlace de perfil.
    """
    name = models.CharField(max_length=255)
    href = models.URLField()

    def __str__(self):
        return self.name

class PersonalInfo(models.Model):
    """
    Modelo que almacena información personal del docente.
    """
    entry = models.OneToOneField(Entry, on_delete=models.CASCADE, related_name="personal_info")
    nombre = models.CharField(max_length=255, blank=True, null=True)
    nombre_citaciones = models.CharField(max_length=255, blank=True, null=True)  
    categoria = models.CharField(max_length=255, blank=True, null=True)  
    par_evaluador = models.BooleanField(default=False)  
    nacionalidad = models.CharField(max_length=100, blank=True, null=True)
    sexo = models.CharField(max_length=50, blank=True, null=True)  

    def __str__(self):
        return f"{self.nombre} - {self.entry.name}"

class Investigacion(models.Model):
    """
    Modelo que almacena las investigaciones relacionadas con un docente.
    """
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="investigaciones")
    titulo = models.CharField(max_length=500)
    tipo = models.CharField(max_length=255, blank=True, null=True)
    fecha = models.CharField(max_length=100, blank=True, null=True)
    institucion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.entry.name} - {self.titulo}"

class FormacionAcademica(models.Model):
    """
    Modelo que almacena la formación académica principal de un docente.
    """
    entry = models.OneToOneField(Entry, on_delete=models.CASCADE, related_name="formacion_academica")
    nivel = models.CharField(max_length=255)
    institucion = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.entry.name} - {self.nivel}"

class ExperienciaProfesional(models.Model):
    """
    Modelo que almacena la experiencia profesional principal de un docente.
    """
    entry = models.OneToOneField(Entry, on_delete=models.CASCADE, related_name="experiencia_profesional")
    institucion = models.CharField(max_length=255)
    cargo = models.CharField(max_length=255)
    desde = models.CharField(max_length=100, blank=True, null=True)
    hasta = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.entry.name} - {self.cargo} en {self.institucion}"
