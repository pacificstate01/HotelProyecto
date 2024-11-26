# Generated by Django 5.1 on 2024-11-23 22:30

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('numero_documento', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True, verbose_name='Número de Documento')),
                ('tipo_documento', models.CharField(choices=[('DNI', 'DNI'), ('PASAPORTE', 'Pasaporte'), ('RUT', 'RUT')], max_length=20, verbose_name='Tipo de Documento')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('apellido', models.CharField(max_length=50, verbose_name='Apellido')),
                ('telefono', models.CharField(blank=True, max_length=9, null=True, verbose_name='Teléfono')),
                ('correo', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electrónico')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de Última Actualización')),
            ],
        ),
        migrations.CreateModel(
            name='Habitacion',
            fields=[
                ('numero_habitacion', models.PositiveIntegerField(primary_key=True, serialize=False, verbose_name='Número de Habitación')),
                ('tipo_habitacion', models.CharField(choices=[('SIMPLE', 'Simple'), ('DOBLE', 'Doble'), ('SUITE', 'Suite')], max_length=50, verbose_name='Tipo de Habitación')),
                ('estado_habitacion', models.CharField(choices=[('DISPONIBLE', 'Disponible'), ('OCUPADA', 'Ocupada'), ('LIMPIEZA', 'Limpieza')], default='DISPONIBLE', max_length=20, verbose_name='Estado de la Habitación')),
                ('precio_habitacion', models.PositiveIntegerField(verbose_name='Precio')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de Última Actualización')),
            ],
        ),
        migrations.CreateModel(
            name='TipoUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='techs')),
                ('tipo_usuario', models.CharField(choices=[('ADMINISTRADOR', 'Administrador de Hotel'), ('ENCARGADO', 'Encargado de Hotel'), ('AUXILIAR', 'Auxiliar de Aseo')], max_length=20, verbose_name='Tipo de Usuario')),
                ('codigo_usuario', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='Código de Usuario')),
                ('direccion', models.CharField(blank=True, max_length=100, null=True, verbose_name='Dirección')),
                ('telefono', models.IntegerField(blank=True, null=True, verbose_name='Teléfono')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de Última Actualización')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('codigo_reserva', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('estado_reserva', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('CONFIRMADA', 'Confirmada'), ('CANCELADA', 'Cancelada')], default='PENDIENTE', max_length=20, verbose_name='Estado de Reserva')),
                ('FechaEntrada', models.DateTimeField(blank=True, null=True)),
                ('FechaSalida', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de Última Actualización')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Hotel.client', verbose_name='Cliente')),
                ('habitaciones', models.ManyToManyField(to='Hotel.habitacion', verbose_name='Habitaciones')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='encargado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
    ]
