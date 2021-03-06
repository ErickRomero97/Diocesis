# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-11-26 19:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0005_homilia_titulo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_album', models.CharField(max_length=100)),
                ('fecha_pub', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Publicacion')),
            ],
        ),
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='galeria')),
            ],
        ),
    ]
