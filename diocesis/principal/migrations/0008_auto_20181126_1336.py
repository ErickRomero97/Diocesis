# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-11-26 19:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0007_auto_20181126_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='imagen',
            field=models.ManyToManyField(blank=True, to='principal.Imagen'),
        ),
    ]
