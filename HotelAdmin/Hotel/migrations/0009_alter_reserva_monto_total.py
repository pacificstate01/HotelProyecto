# Generated by Django 5.1 on 2024-12-12 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hotel', '0008_reserva_habitaciones_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='monto_total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Monto Total'),
        ),
    ]
