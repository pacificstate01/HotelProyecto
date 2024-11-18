# Generated by Django 5.1 on 2024-11-18 00:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hotel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FechaHoraEntradas', models.DateTimeField(blank=True, null=True)),
                ('FechaSalida', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='tipousuario',
            name='telefono',
            field=models.IntegerField(blank=True, null=True, verbose_name='Teléfono'),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('numero_documento', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True, verbose_name='Número de Documento')),
                ('tipo_documento', models.CharField(choices=[('DNI', 'DNI'), ('PASAPORTE', 'Pasaporte'), ('RUT', 'RUT')], max_length=20, verbose_name='Tipo de Documento')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('apellido', models.CharField(max_length=50, verbose_name='Apellido')),
                ('telefono', models.IntegerField(blank=True, null=True, verbose_name='Teléfono')),
                ('correo', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electrónico')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de Última Actualización')),
                ('encargado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
