# Generated by Django 5.1.6 on 2025-03-02 23:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Investigacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('tipo', models.CharField(blank=True, max_length=100, null=True)),
                ('fecha', models.CharField(blank=True, max_length=50, null=True)),
                ('institucion', models.CharField(blank=True, max_length=255, null=True)),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.entry')),
            ],
        ),
        migrations.CreateModel(
            name='PersonalInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=255, null=True)),
                ('identificacion', models.CharField(blank=True, max_length=100, null=True)),
                ('nacionalidad', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('telefono', models.CharField(blank=True, max_length=50, null=True)),
                ('entry', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scraping.entry')),
            ],
        ),
        migrations.DeleteModel(
            name='ExtractedData',
        ),
    ]
