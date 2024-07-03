# Generated by Django 5.0.6 on 2024-06-19 17:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('href', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='ExtractedData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.entry')),
            ],
        ),
    ]
