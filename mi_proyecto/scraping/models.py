from django.db import models

class Entry(models.Model):
    name = models.CharField(max_length=255)
    href = models.URLField()

class ExtractedData(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    data = models.JSONField()
