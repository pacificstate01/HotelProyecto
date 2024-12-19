import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from datetime import datetime
import numpy as np
from io import BytesIO
from .models import Habitacion, Reserva
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

def generar_reporte_ocupacion():
    # Obtener y ordenar todos los números de habitación de menor a mayor
    habitaciones = sorted(Habitacion.objects.values_list('numero_habitacion', flat=True))
    dias_mes = range(1, 32)  # Días del mes (1 al 31)

    # Obtener todas las reservas del mes actual
    reservas = Reserva.objects.filter(
        original_FechaEntrada__month=datetime.now().month
    ).prefetch_related('habitaciones')

    # Crear la matriz de disponibilidad (0 = libre, 1 = ocupada)
    disponibilidad = np.zeros((len(habitaciones), len(dias_mes)))

    # Guardar los bloques de reservas
    reservas_bloques = []

    # Marcar los días ocupados por las reservas
    for reserva in reservas:
        for habitacion in reserva.habitaciones.all():
            try:
                # Obtener el índice de la habitación en la lista ordenada
                habitacion_idx = habitaciones.index(habitacion.numero_habitacion)
                fecha_inicio = reserva.original_FechaEntrada.day
                fecha_fin = reserva.original_FechaSalida.day

                # Guardar bloques para dibujar rectángulos
                reservas_bloques.append((habitacion_idx, fecha_inicio - 1, fecha_fin - 1))

                # Marcar los días ocupados
                disponibilidad[habitacion_idx, fecha_inicio - 1:fecha_fin] = 1
            except ValueError:
                continue

    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(11, 6))
    cax = ax.imshow(disponibilidad, cmap="PuBu", aspect="auto",
                    extent=[1.7, len(dias_mes) - 1.1, len(habitaciones) - 0, -0])

    # Dibujar contornos para las reservas
    for habitacion_idx, inicio, fin in reservas_bloques:
        rect = Rectangle(
            (inicio, habitacion_idx),  # Coordenada de inicio ajustada
            fin - inicio,  # Ancho
            1,  # Alto (una fila por habitación)
            linewidth=2.8,
            edgecolor="red",
            facecolor="none"
        )
        ax.add_patch(rect)

    # Agregar cuadrícula para mayor legibilidad
    ax.set_xticks(np.arange(1, len(dias_mes) + 1))
    ax.set_yticks(np.arange(1, len(habitaciones) + 1))
    ax.grid(color="black", linestyle="--", linewidth=0.5, alpha=0.3)

# Etiquetas para el gráfico
    ax.set_yticks(np.arange(len(habitaciones)) + 0.5)  # Centrar los números en la mitad
    ax.set_yticklabels(habitaciones)  # Mostrar el número de la habitación
    ax.set_xticks(np.arange(len(dias_mes)))  # Asegurar que los días estén en el centro
    ax.set_xticklabels(dias_mes)  # Etiquetas de los días

    ax.set_xlabel("Días del mes")
    ax.set_ylabel("Habitaciones")
    ax.set_title("Reporte de ocupación de habitaciones")
    plt.colorbar(cax, label="Estado (0=Libre, 1=Ocupado)")

    # Convertir el gráfico a una imagen
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return buffer