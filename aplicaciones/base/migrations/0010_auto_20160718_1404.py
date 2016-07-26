# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-18 14:04
from __future__ import unicode_literals

import aplicaciones.base.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_auto_20160717_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='codigoverificacion',
            name='fechaEmision',
            field=models.DateField(default=datetime.datetime.now, verbose_name='fecha de emisión'),
        ),
        migrations.AlterField(
            model_name='codigoverificacion',
            name='fechaVencimiento',
            field=models.DateField(default=aplicaciones.base.models.fecha_vencimiento_defecto, verbose_name='fecha de vencimiento'),
        ),
    ]