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
    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name="Teléfono")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Última Actualización")



    def get_full_name(self):
        return f"{self.name} {self.last_name}"


class Reserva(models.Model):
    FechaHoraEntradas = models.DateTimeField(null=True, blank=True)
    FechaSalida = models.DateField(null=True, blank=True)
    def __str__(self):
        return f"Reserva from {self.FechaHoraEntradas} to {self.FechaSalida}"