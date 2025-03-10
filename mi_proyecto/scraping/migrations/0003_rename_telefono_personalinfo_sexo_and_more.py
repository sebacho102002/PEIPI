# Generated by Django 5.1.6 on 2025-03-06 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0002_investigacion_personalinfo_delete_extracteddata'),
    ]

    operations = [
        migrations.RenameField(
            model_name='personalinfo',
            old_name='telefono',
            new_name='sexo',
        ),
        migrations.RemoveField(
            model_name='personalinfo',
            name='email',
        ),
        migrations.RemoveField(
            model_name='personalinfo',
            name='identificacion',
        ),
        migrations.AddField(
            model_name='personalinfo',
            name='categoria',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='personalinfo',
            name='nombre_citaciones',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='personalinfo',
            name='par_evaluador',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='investigacion',
            name='fecha',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='investigacion',
            name='tipo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='investigacion',
            name='titulo',
            field=models.CharField(max_length=500),
        ),
    ]
