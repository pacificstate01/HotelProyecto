# admin.py
from django.contrib import admin
from .models import TipoUsuario,Client,Reserva
admin.site.register(TipoUsuario)
admin.site.register(Client)
admin.site.register(Reserva)
