# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-04 18:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0014_parroquia_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pastoral',
            name='eslogan',
            field=models.TextField(),
        ),
    ]
