# Generated by Django 5.1 on 2024-11-18 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hotel', '0002_reserva_alter_tipousuario_telefono_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='telefono',
            field=models.CharField(blank=True, max_length=9, null=True, verbose_name='Teléfono'),
        ),
    ]