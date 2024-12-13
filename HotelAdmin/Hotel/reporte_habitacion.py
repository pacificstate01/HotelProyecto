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
    # Obtener todos los números de habitación
    habitaciones = list(Habitacion.objects.values_list('numero_habitacion', flat=True))
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
    fig, ax = plt.subplots(figsize=(12, 6))
    cax = ax.imshow(disponibilidad, cmap="Greens", aspect="auto")

    # Dibujar contornos para las reservas
    for habitacion_idx, inicio, fin in reservas_bloques:
        rect = Rectangle(
            (inicio - 0.5, habitacion_idx - 0.5),  # Coordenada de inicio ajustada
            fin - inicio + 1,  # Ancho
            1,  # Alto (una fila por habitación)
            linewidth=2,
            edgecolor="blue",
            facecolor="none"
        )
        ax.add_patch(rect)

    # Etiquetas para el gráfico
    ax.set_yticks(range(len(habitaciones)))
    ax.set_yticklabels(habitaciones)
    ax.set_xticks(range(len(dias_mes)))
    ax.set_xticklabels(dias_mes)
    ax.set_xlabel("Días del mes")
    ax.set_ylabel("Habitaciones")
    ax.set_title("Reporte de ocupación de habitaciones")
    plt.colorbar(cax, label="Estado (0=Libre, 1=Ocupado)")

    # Convertir el gráfico a una imagen
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return buffer
