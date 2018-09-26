# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-09-24 22:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aquifers', '0002_aquifers_codes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aquifer',
            name='aquifer_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='aquifer',
            name='litho_stratographic_unit',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Lithographic Stratographic Unit'),
        ),
        migrations.AlterField(
            model_name='aquifer',
            name='location_description',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Description of Location'),
        ),
    ]
