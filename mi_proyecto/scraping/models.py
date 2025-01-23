from django.db import models

class Entry(models.Model):
    name = models.CharField(max_length=255)
    href = models.URLField()


class ExtractedData(models.Model):
    entry = models.ForeignKey('Entry', related_name='extracteddata_set', on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    value = models.TextField()

    def __str__(self):
        return f"{self.key}: {self.value}"
