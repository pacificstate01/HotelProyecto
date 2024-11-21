from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid



class TipoUsuario(AbstractUser):
    TIPO_USUARIO = [
        ('ADMINISTRADOR', 'Administrador de Hotel'),
        ('ENCARGADO', 'Encargado de Hotel'),
        ('AUXILIAR', 'Auxiliar de Aseo'),
    ]
    name= models.CharField(max_length=200)
    last_name= models.CharField(max_length=200)
    avatar = models.ImageField(null=True, blank=True,upload_to="techs")
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO, verbose_name="Tipo de Usuario")
    codigo_usuario = models.UUIDField(default=uuid.uuid4, unique=True, verbose_name="Código de Usuario")
    direccion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Dirección")
    telefono = models.IntegerField(blank=True, null=True, verbose_name="Teléfono")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Última Actualización")



    def get_full_name(self):
        return f"{self.name} {self.last_name}"


class Client(models.Model):
    TIPO_DOCUMENTO = [
        ('DNI', 'DNI'),
        ('PASAPORTE', 'Pasaporte'),
        ('RUT', 'RUT'),
    ]

    numero_documento = models.CharField(max_length=20, unique=True, primary_key=True, verbose_name="Número de Documento")
    tipo_documento = models.CharField(max_length=20, choices=TIPO_DOCUMENTO, verbose_name="Tipo de Documento")
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    apellido = models.CharField(max_length=50, verbose_name="Apellido")
    telefono = models.CharField(max_length=9,blank=True, null=True, verbose_name="Teléfono")
    correo = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Última Actualización")
    encargado = models.ForeignKey(TipoUsuario,null=True,blank=True,on_delete=models.RESTRICT)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Habitacion(models.Model):
    ESTADO_HABITACION = [
        ('DISPONIBLE', 'Disponible'),
        ('OCUPADA', 'Ocupada'),
        ('LIMPIEZA', 'Limpieza'),
    ]
    TIPO_HABITACION = [
        ('SIMPLE', 'Simple'),
        ('DOBLE', 'Doble'),
        ('SUITE', 'Suite'),
    ]

    numero_habitacion = models.PositiveIntegerField(primary_key=True, verbose_name="Número de Habitación")
    tipo_habitacion = models.CharField(max_length=50, choices=TIPO_HABITACION, verbose_name="Tipo de Habitación")
    estado_habitacion = models.CharField(max_length=20, choices=ESTADO_HABITACION, default='DISPONIBLE', verbose_name="Estado de la Habitación")
    precio_habitacion = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Última Actualización")


    def __str__(self):
        return f"Habitación {self.numero_habitacion} - {self.tipo_habitacion}"




class Reserva(models.Model):
    FechaHoraEntradas = models.DateTimeField(null=True, blank=True)
    FechaSalida = models.DateField(null=True, blank=True)
    def __str__(self):
        return f"Reserva from {self.FechaHoraEntradas} to {self.FechaSalida}"