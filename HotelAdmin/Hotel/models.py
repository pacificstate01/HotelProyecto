from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid
from django.core.validators import MinValueValidator
from datetime import datetime, time,date

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

    numero_habitacion = models.PositiveIntegerField(unique=True,verbose_name="Número de Habitación")
    tipo_habitacion = models.CharField(max_length=50, choices=TIPO_HABITACION, verbose_name="Tipo de Habitación")
    estado_habitacion = models.CharField(max_length=20, choices=ESTADO_HABITACION, default='DISPONIBLE', verbose_name="Estado de la Habitación")
    precio_habitacion = models.PositiveIntegerField(validators=[MinValueValidator(1)],verbose_name="Precio")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Última Actualización")

    def __str__(self):
        return f"Habitación {self.numero_habitacion} - {self.tipo_habitacion}"




from datetime import date
from django.core.exceptions import ValidationError
from django.db import models
import uuid


class Reserva(models.Model):
    ESTADO_RESERVA = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
        ('CHECK-OUT', 'Check-Out'),
    ]

    codigo_reserva = models.AutoField(primary_key=True, unique=True)
    estado_reserva = models.CharField(max_length=20, choices=ESTADO_RESERVA, default='PENDIENTE', verbose_name="Estado de Reserva")
    FechaEntrada = models.DateField(null=True, blank=True)
    FechaSalida = models.DateField(null=True, blank=True)
    original_FechaEntrada = models.DateField(blank=True, null=True)
    original_FechaSalida = models.DateField(blank=True, null=True)
    habitaciones = models.ManyToManyField(Habitacion, verbose_name="Habitaciones")
    cliente = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name="Cliente")
    usuario = models.ForeignKey(TipoUsuario, on_delete=models.PROTECT, verbose_name="Usuario")
    detallesRev = models.TextField(blank=True, verbose_name="Detalles reserva")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Última Actualización")
    codigo_factura = models.CharField(max_length=20, unique=True, null=True, blank=True)
    fecha_emision = models.DateField(auto_now_add=True, verbose_name="Fecha de Emisión", null=True, blank=True)
    habitaciones_count = models.PositiveIntegerField(default=0, editable=False)

    def clean(self):
        if not self.FechaEntrada or not self.FechaSalida:
            raise ValidationError("Las fechas de entrada y salida deben ser proporcionadas.")
        
        if self.FechaSalida <= self.FechaEntrada:
            raise ValidationError("La fecha de salida debe ser posterior a la fecha de entrada.")
        
        if self.pk: 
            overlapping_reservations = Reserva.objects.filter(
                FechaEntrada__lt=self.FechaSalida,
                FechaSalida__gt=self.FechaEntrada,
                estado_reserva__in=['PENDIENTE', 'CONFIRMADA']
            ).exclude(codigo_reserva=self.codigo_reserva)

            for habitacion in self.habitaciones.all():
                for reserva in overlapping_reservations:
                    if habitacion in reserva.habitaciones.all():
                        raise ValidationError(f"La habitación {habitacion.numero_habitacion} ya está reservada en esas fechas.")
        
        super().clean()

    def save(self, *args, **kwargs):
        if not self.codigo_factura:
            self.codigo_factura = str(uuid.uuid4())[:8]  

        if not self.pk:
            super().save(*args, **kwargs)
        if self.estado_reserva == 'CONFIRMADA':
            Habitacion.objects.filter(id__in=[h.id for h in self.habitaciones.all()]).update(estado_habitacion='OCUPADA')
        if not self.original_FechaEntrada and not self.original_FechaSalida:
            self.original_FechaEntrada = self.FechaEntrada
            self.original_FechaSalida = self.FechaSalida
        
        if self.estado_reserva == 'CANCELADA' or self.estado_reserva == 'CHECK-OUT':
            self.FechaEntrada = date(1900, 1, 1)
            self.FechaSalida = date(1900, 1, 1)
        
        super().save(*args, **kwargs)

    def get_display_fecha_entrada(self):
        return self.original_FechaEntrada if self.original_FechaEntrada else self.FechaEntrada

    def get_display_fecha_salida(self):
        return self.original_FechaSalida if self.original_FechaSalida else self.FechaSalida

    def __str__(self):
        return f"Reserva {self.codigo_reserva} - {self.estado_reserva} - Habitaciones: {self.habitaciones_count}"
