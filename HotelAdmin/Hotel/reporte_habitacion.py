# Hotel/reportes.py
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg') 
import numpy as np
from io import BytesIO
from datetime import datetime
from Hotel.models import Reserva, Habitacion

def generar_reporte_ocupacion():
    # Obtener todos los números de habitación
    habitaciones = list(Habitacion.objects.values_list('numero_habitacion', flat=True))
    dias_mes = range(1, 32)  # Días del mes (1 al 31)

    # Obtener las reservas del mes actual
    reservas = Reserva.objects.filter(
        FechaEntrada__month=datetime.now().month  # Filtrar por el mes actual
    ).prefetch_related('habitaciones')  # Optimizar con prefetch_related para obtener las habitaciones

    # Crear la matriz de disponibilidad (0 = libre, 1 = ocupada)
    disponibilidad = np.zeros((len(habitaciones), len(dias_mes)))

    # Marcar los días ocupados por las reservas
    for reserva in reservas:
        # Iterar sobre las habitaciones asociadas a la reserva
        for habitacion in reserva.habitaciones.all():
            habitacion_idx = habitaciones.index(habitacion.numero_habitacion)  # Obtener el índice de la habitación
            fecha_inicio = reserva.FechaEntrada.day  # Día de inicio de la reserva
            fecha_fin = reserva.FechaSalida.day  # Día de fin de la reserva

            # Marcar los días de la reserva como ocupados (1)
            for dia in range(fecha_inicio, fecha_fin + 1):
                disponibilidad[habitacion_idx, dia - 1] = 1

    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(12, 6))
    cax = ax.imshow(disponibilidad, cmap="Greens", aspect="auto")

    # Etiquetas para el gráfico
    ax.set_yticks(range(len(habitaciones)))
    ax.set_yticklabels(habitaciones)
    ax.set_xticks(range(len(dias_mes)))
    ax.set_xticklabels(dias_mes)
    ax.set_xlabel("Días del mes")
    ax.set_ylabel("Habitaciones")
    ax.set_title("Reporte de ocupación de habitaciones")
    plt.colorbar(cax, label="Estado (0=Libre, 1=Ocupado)")

    # Convertir el gráfico en una imagen para el navegador
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return buffer