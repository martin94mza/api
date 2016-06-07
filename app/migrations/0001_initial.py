# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-29 00:23
from __future__ import unicode_literals

import app.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaEvento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField(blank=True, verbose_name='descripción')),
            ],
            options={
                'verbose_name_plural': 'categorías del evento',
                'verbose_name': 'categoría del evento',
            },
        ),
        migrations.CreateModel(
            name='CentroDonacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'centros de donación',
                'verbose_name': 'centro de donación',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='DetalleRegistroDonacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaHora', models.DateTimeField(verbose_name='fecha y hora')),
                ('foto', models.ImageField(blank=True, upload_to='')),
                ('descripcion', models.TextField(blank=True, verbose_name='descripción')),
                ('centroDonacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.CentroDonacion', verbose_name='centro de donación')),
            ],
            options={
                'verbose_name_plural': 'detalles del registro de donación',
                'verbose_name': 'detalle del registro de donación',
            },
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calle', models.CharField(max_length=50)),
                ('numero', models.PositiveSmallIntegerField(verbose_name='número')),
                ('piso', models.SmallIntegerField(blank=True, null=True)),
                ('numeroDepartamento', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='número de departamento')),
            ],
            options={
                'verbose_name_plural': 'direcciones',
                'verbose_name': 'dirección',
            },
        ),
        migrations.CreateModel(
            name='Donante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('telefono', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="El número de teléfono debe estar en el siguiente formato: '+999999999'. Se permiten un máximo de 15 dígitos.", regex='^\\+?1?\\d{9,15}$')], verbose_name='teléfono')),
                ('nacimiento', models.DateField(verbose_name='fecha de nacimiento')),
                ('peso', models.DecimalField(decimal_places=1, max_digits=4)),
                ('altura', models.DecimalField(decimal_places=2, max_digits=3)),
                ('genero', app.models.GenerosField(choices=[('1', 'Masculino'), ('2', 'Femenino')], max_length=1, verbose_name='género')),
                ('direccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Direccion', verbose_name='dirección')),
            ],
        ),
        migrations.CreateModel(
            name='EstadoSolicitudDonacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('descripcion', models.TextField(blank=True, verbose_name='descripción')),
            ],
            options={
                'verbose_name_plural': 'estados de solicitud de donación',
                'verbose_name': 'estado de solicitud de donación',
            },
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('fechaHoraInicio', models.DateTimeField(verbose_name='fecha y hora de inicio')),
                ('fechaHoraFin', models.DateTimeField(verbose_name='fecha y hora de finalización')),
                ('descripcion', models.TextField(blank=True, verbose_name='descripción')),
                ('video', models.FileField(upload_to='')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.CategoriaEvento', verbose_name='categoría del evento')),
                ('centroDonacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.CentroDonacion', verbose_name='centro de donación')),
            ],
        ),
        migrations.CreateModel(
            name='GrupoSanguineo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=5)),
                ('puedeDonarA', models.ManyToManyField(blank=True, related_name='_gruposanguineo_puedeDonarA_+', to='app.GrupoSanguineo', verbose_name='puede donar a')),
            ],
            options={
                'verbose_name_plural': 'grupos sanguíneos',
                'verbose_name': 'grupo sanguíneo',
            },
        ),
        migrations.CreateModel(
            name='GrupoSanguineoSolicitud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grupoSanguineo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.GrupoSanguineo', verbose_name='grupo sanguíneo')),
            ],
            options={
                'verbose_name_plural': 'grupos sanguíneos de la solicitud de donación',
                'verbose_name': 'grupo sanguíneo de la solicitud de donación',
            },
        ),
        migrations.CreateModel(
            name='HorarioCentroDonacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', app.models.DiasSemanaField(choices=[('1', 'Lunes'), ('2', 'Martes'), ('3', 'Miércoles'), ('4', 'Jueves'), ('5', 'Viernes'), ('6', 'Sábado'), ('7', 'Domingo')], max_length=1)),
                ('horaApertura', models.TimeField(verbose_name='hora de apertura')),
                ('horaCierre', models.TimeField(verbose_name='hora de cierre')),
            ],
            options={
                'verbose_name_plural': 'horarios del centro de donación',
                'verbose_name': 'horario del centro de donación',
            },
        ),
        migrations.CreateModel(
            name='ImagenEvento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='')),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Evento')),
            ],
            options={
                'verbose_name_plural': 'imágenes del evento',
                'verbose_name': 'imagen del evento',
            },
        ),
        migrations.CreateModel(
            name='ImagenSolicitudDonacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='')),
            ],
            options={
                'verbose_name_plural': 'imágenes de solicitud de donación',
                'verbose_name': 'imagen de solicitud de donación',
            },
        ),
        migrations.CreateModel(
            name='Localidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'localidades',
                'verbose_name': 'localidad',
            },
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('nacimiento', models.DateField(verbose_name='fecha de nacimiento')),
                ('telefono', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="El número de teléfono debe estar en el siguiente formato: '+999999999'. Se permiten un máximo de 15 dígitos.", regex='^\\+?1?\\d{9,15}$')], verbose_name='teléfono')),
                ('genero', app.models.GenerosField(choices=[('1', 'Masculino'), ('2', 'Femenino')], max_length=1)),
                ('direccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Direccion', verbose_name='dirección')),
            ],
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RegistroDonacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('privado', models.BooleanField(default=True)),
                ('donante', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.Donante')),
            ],
            options={
                'verbose_name_plural': 'registros de donación',
                'verbose_name': 'registro de donación',
            },
        ),
        migrations.CreateModel(
            name='SolicitudDonacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('fechaPublicacion', models.DateField(verbose_name='fecha de publicación')),
                ('donantesNecesarios', models.SmallIntegerField(verbose_name='cantidad de donantes necesarios')),
                ('video', models.FileField(upload_to='')),
                ('fechaHoraInicio', models.DateTimeField(verbose_name='fecha y hora de inicio')),
                ('fechaHoraFin', models.DateTimeField(verbose_name='fecha y hora de fin')),
                ('centroDonacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.CentroDonacion', verbose_name='centro de donación')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.EstadoSolicitudDonacion', verbose_name='estado de solicitud de donación')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Paciente')),
            ],
            options={
                'verbose_name_plural': 'solicitudes de donación',
                'verbose_name': 'solicitud de donación',
            },
        ),
        migrations.CreateModel(
            name='TipoCentroDonacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField(blank=True, verbose_name='descripción')),
            ],
            options={
                'verbose_name_plural': 'tipos de centro de donación',
                'verbose_name': 'tipo de centro de donación',
            },
        ),
        migrations.CreateModel(
            name='TipoSolicitudDonacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('descripcion', models.TextField(blank=True, verbose_name='descripción')),
            ],
            options={
                'verbose_name_plural': 'tipos de solicitud de donación',
                'verbose_name': 'tipo de solicitud de donación',
            },
        ),
        migrations.CreateModel(
            name='Verificacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='')),
                ('codigo', models.CharField(max_length=20, verbose_name='código')),
                ('aceptado', models.BooleanField()),
            ],
            options={
                'verbose_name_plural': 'verificaciones',
                'verbose_name': 'verificación',
            },
        ),
        migrations.AddField(
            model_name='solicituddonacion',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.TipoSolicitudDonacion', verbose_name='tipo de solicitud de donación'),
        ),
        migrations.AddField(
            model_name='localidad',
            name='provincia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Provincia'),
        ),
        migrations.AddField(
            model_name='imagensolicituddonacion',
            name='solicitud',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.SolicitudDonacion'),
        ),
        migrations.AddField(
            model_name='gruposanguineosolicitud',
            name='solicitud',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.SolicitudDonacion'),
        ),
        migrations.AddField(
            model_name='donante',
            name='grupoSanguineo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.GrupoSanguineo', verbose_name='grupo sanguíneo'),
        ),
        migrations.AddField(
            model_name='donante',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='direccion',
            name='localidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Localidad'),
        ),
        migrations.AddField(
            model_name='detalleregistrodonacion',
            name='evento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Evento'),
        ),
        migrations.AddField(
            model_name='detalleregistrodonacion',
            name='registro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.RegistroDonacion', verbose_name='registro de donación'),
        ),
        migrations.AddField(
            model_name='detalleregistrodonacion',
            name='verificacion',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Verificacion', verbose_name='verificación'),
        ),
        migrations.AddField(
            model_name='centrodonacion',
            name='direccion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Direccion', verbose_name='dirección'),
        ),
        migrations.AddField(
            model_name='centrodonacion',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.TipoCentroDonacion'),
        ),
    ]
