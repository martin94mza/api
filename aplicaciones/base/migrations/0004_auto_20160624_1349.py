# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-24 16:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20160624_1344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donante',
            name='dni',
        ),
        migrations.AddField(
            model_name='donante',
            name='numeroDocumento',
            field=models.PositiveIntegerField(default=123456789, unique=True, verbose_name='número de documento'),
            preserve_default=False,
        ),
    ]
