# Importaciones y dependencias necesarias
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from weasyprint import HTML
from django.template.loader import render_to_string
from datetime import datetime, timedelta
import base64
from .reporte_habitacion import generar_reporte_ocupacion
from .models import TipoUsuario, Reserva, Client, Habitacion
from .forms import ReservaForm, ClientForm, RoomForm

# Vista del panel principal que muestra estadísticas
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'Hotel/dashboard.html'

    # Obtiene datos de contexto para mostrar estadísticas en el panel
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pendiente'] = Reserva.objects.filter(estado_reserva='PENDIENTE').count()  # Reservas pendientes
        context['disponible'] = Habitacion.objects.filter(estado_habitacion='DISPONIBLE').count()  # Habitaciones disponibles
        context['ocupado'] = Habitacion.objects.filter(estado_habitacion='OCUPADA').count()  # Habitaciones ocupadas
        context['limpieza'] = Habitacion.objects.filter(estado_habitacion='LIMPIEZA').count()  # Habitaciones en limpieza
        # Calcula el total de habitaciones sumando los diferentes estados
        context['total'] = (Habitacion.objects.filter(estado_habitacion='DISPONIBLE').count() + 
                            Habitacion.objects.filter(estado_habitacion='OCUPADA').count() + 
                            Habitacion.objects.filter(estado_habitacion='LIMPIEZA').count())
        return context

# Vista para mostrar las reservas de los clientes
class ClientsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Reserva
    template_name = 'Hotel/reporte_clientes.html'
    context_object_name = 'clients'

    # Restringe acceso solo a administradores, encargados o superusuarios
    def test_func(self):
        return self.request.user.tipo_usuario in ['ADMINISTRADOR', 'ENCARGADO'] or self.request.user.is_superuser   

    # Maneja el acceso no autorizado
    def handle_no_permission(self):
        return render(self.request, 'Hotel/sin_permiso.html', status=403)

    # Optimiza consultas a la base de datos para mejorar el rendimiento
    def get_queryset(self):
        reservas = Reserva.objects.prefetch_related(
            'habitaciones',  # Carga las habitaciones relacionadas
            'cliente'        # Carga el cliente relacionado
        ).filter(FechaEntrada__month=datetime.now().month)  # Filtra por el mes actual
        return reservas

# Vista para mostrar reportes de habitaciones
class ReporteHabitaciones(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Reserva
    template_name = 'Hotel/reporte_habitaciones.html'
    context_object_name = 'habitaciones'

    # Restringe acceso solo a administradores, encargados o superusuarios
    def test_func(self):
        return self.request.user.tipo_usuario in ['ADMINISTRADOR', 'ENCARGADO'] or self.request.user.is_superuser   

    # Maneja el acceso no autorizado
    def handle_no_permission(self):
        return render(self.request, 'Hotel/sin_permiso.html', status=403)

# Vista para gestionar la información de habitaciones
class ManageRoomsView(LoginRequiredMixin, ListView):
    model = Habitacion
    template_name = 'Hotel/gestion_habitaciones.html'
    context_object_name = 'rooms'

    # Agrega el formulario para gestionar habitaciones al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RoomForm()
        return context

# Vista para crear una nueva habitación
class ManageRoomCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Habitacion
    form_class = RoomForm

    # Restringe acceso solo a administradores, encargados o superusuarios
    def test_func(self):
        return self.request.user.tipo_usuario in ['ADMINISTRADOR', 'ENCARGADO'] or self.request.user.is_superuser   

    # Maneja el acceso no autorizado
    def handle_no_permission(self):
        return render(self.request, 'Hotel/sin_permiso.html', status=403)

    # Maneja la creación exitosa de una habitación con respuesta JSON
    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({'success': True, 'message': 'Habitación creada correctamente!'})

    # Maneja errores de validación del formulario con respuesta JSON
    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors})


# Clase para eliminar habitaciones
class ManageRoomDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Habitacion
    success_url = reverse_lazy('gestion_hab')  # URL a redirigir tras eliminar

    # Verifica si el usuario tiene permisos para esta acción
    def test_func(self):
        return self.request.user.tipo_usuario == 'ADMINISTRADOR' or self.request.user.tipo_usuario == 'ENCARGADO' or self.request.user.is_superuser   

    # Maneja el acceso no autorizado mostrando una página personalizada
    def handle_no_permission(self):
        return render(self.request, 'Hotel/sin_permiso.html', status=403)

    # Obtiene la habitación a eliminar, con validación de estado
    def get_object(self, queryset=None):
        room = super().get_object(queryset)
        if room.estado_habitacion == 'OCUPADA':  # Valida si la habitación está ocupada
            self.room_error = 'Habitación ocupada, no se puede eliminar.'
            return None
        return room

    # Método para eliminar la habitación con respuesta personalizada
    def delete(self, request, *args, **kwargs):
        room = self.get_object()
        if room is None:  # Maneja el caso de error al intentar eliminar
            return JsonResponse({'error': self.room_error}, status=403)
        return super().delete(request, *args, **kwargs)

# Clase para actualizar habitaciones
class ManageRoomUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Habitacion
    fields = ['tipo_habitacion', 'precio_habitacion']  # Campos permitidos para actualizar
    template_name = 'Hotel/Habitaciones/room_update.html'
    success_url = reverse_lazy('gestion_hab')  # URL a redirigir tras actualizar

    # Verifica permisos para actualizar
    def test_func(self):
        return self.request.user.tipo_usuario == 'ADMINISTRADOR' or self.request.user.tipo_usuario == 'ENCARGADO' or self.request.user.is_superuser    

    # Maneja el acceso no autorizado mostrando una página personalizada
    def handle_no_permission(self):
        return render(self.request, 'Hotel/sin_permiso.html', status=403)

    # Valida y guarda el formulario
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    # Personaliza los widgets del formulario
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['tipo_habitacion'].widget.attrs.update({'class': 'form-control'})
        form.fields['precio_habitacion'].widget.attrs.update({'class': 'form-control'})
        return form

# Clase para cambiar el estado de una habitación
class CambiarEstadoHab(View):
    # Cambia el estado de "LIMPIEZA" a "DISPONIBLE"
    def post(self, request, numero_habitacion):
        habitacion = get_object_or_404(Habitacion, numero_habitacion=numero_habitacion)
        if habitacion.estado_habitacion == 'LIMPIEZA':
            habitacion.estado_habitacion = 'DISPONIBLE'
            habitacion.save()  # Guarda el cambio en la base de datos
            messages.success(self.request, f'Habitación número {habitacion.numero_habitacion} actualizada.')
        return redirect('gestion_hab')  # Redirige tras el cambio

# Clase para gestionar clientes
class ManageClientsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Client
    template_name = 'Hotel/gestion_clientes.html'
    context_object_name = 'clients'  # Nombre del contexto para acceder en la plantilla

    # Verifica permisos para acceder a la vista
    def test_func(self):
        return self.request.user.tipo_usuario == 'ADMINISTRADOR' or self.request.user.tipo_usuario == 'ENCARGADO' or self.request.user.is_superuser    

    # Maneja el acceso no autorizado mostrando una página personalizada
    def handle_no_permission(self):
        return render(self.request, 'Hotel/sin_permiso.html', status=403)

    # Agrega datos adicionales al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for client in context['clients']:
            rut = ''.join([c for c in client.numero_documento if c.isdigit()])  # Elimina caracteres no numéricos
            if len(rut) == 9:  # Aplica formato si tiene longitud válida
                client.formatted_numero_documento = f'{rut[:2]}.{rut[2:5]}.{rut[5:8]}-{rut[8]}'
            else:
                client.formatted_numero_documento = client.numero_documento  # Muestra sin formato si no aplica
        return context

# Clase para crear un nuevo cliente
class ClientCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Client
    form_class = ClientForm  # Formulario asociado
    template_name = 'Hotel/create_client.html'
    success_url = reverse_lazy('gestion_cli')  # URL a redirigir tras crear

    # Verifica permisos para crear un cliente
    def test_func(self):
        return self.request.user.tipo_usuario == 'ADMINISTRADOR' or self.request.user.tipo_usuario == 'ENCARGADO' or self.request.user.is_superuser    

    # Maneja el acceso no autorizado mostrando una página personalizada
    def handle_no_permission(self):
        return render(self.request, 'Hotel/sin_permiso.html', status=403)

    # Maneja errores del formulario con respuesta JSON
    def form_invalid(self, form):
        errors = {field: error.get_json_data() for field, error in form.errors.items()}
        return JsonResponse({'success': False, 'errors': errors}, status=400)

    # Maneja la creación exitosa con un mensaje de éxito
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Cliente con número de documento {form.instance.numero_documento} ha sido creado correctamente.')
        return JsonResponse({'success': True, 'message': 'Cliente agregado exitosamente!'})


# Clase para eliminar clientes
class ClientDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('gestion_cli')  # Redirige tras eliminar el cliente
    template_name = None  # No se define plantilla, utiliza la predeterminada

    def test_func(self):
        # Verifica permisos del usuario
        return self.request.user.tipo_usuario in ['ADMINISTRADOR', 'ENCARGADO'] or self.request.user.is_superuser

    def handle_no_permission(self):
        # Página personalizada al no tener permisos
        return render(self.request, 'Hotel/sin_permiso.html', status=403)

    def get_object(self, queryset=None):
        # Obtiene el cliente por su `numero_documento`
        numero_documento = self.kwargs.get('numero_documento')
        return Client.objects.get(numero_documento=numero_documento)

    def form_valid(self, form):
        # Mensaje al eliminar cliente
        numero_documento = self.get_object().numero_documento
        messages.success(self.request, f'Cliente con número de documento {numero_documento} ha sido eliminado correctamente.')
        return super().form_valid(form)


# Clase para actualizar clientes
class ClientUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    fields = ['nombre', 'apellido', 'telefono', 'correo']  # Campos editables
    template_name = 'Hotel/update_client.html'
    success_url = reverse_lazy('gestion_cli')  # Redirige tras actualizar

    def test_func(self):
        # Verifica permisos del usuario
        return self.request.user.tipo_usuario in ['ADMINISTRADOR', 'ENCARGADO'] or self.request.user.is_superuser

    def handle_no_permission(self):
        # Página personalizada al no tener permisos
        return render(self.request, 'Hotel/sin_permiso.html', status=403)

    def get_form(self, *args, **kwargs):
        # Personaliza el formulario y valida el campo teléfono
        form = super().get_form(*args, **kwargs)
        for field in ['nombre', 'apellido', 'telefono', 'correo']:
            form.fields[field].widget.attrs.update({'class': 'form-control'})

        telefono_field = form.fields['telefono']
        telefono_field.required = True
        telefono_field.validators.append(self.validate_telefono)
        return form

    def validate_telefono(self, value):
        # Validación personalizada del teléfono
        if not value:
            raise ValidationError("El número de teléfono es obligatorio.")
        if not value.startswith('9'):
            raise ValidationError("El número debe empezar con 9.")
        if len(value) != 9:
            raise ValidationError("El número debe tener exactamente 9 dígitos.")
        return value

    def get_object(self, queryset=None):
        # Obtiene el cliente por `numero_documento`
        return Client.objects.get(numero_documento=self.kwargs['numero_documento'])

    def form_valid(self, form):
        # Mensaje al actualizar correctamente
        messages.success(self.request, 'Cliente actualizado correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Mensaje en caso de error
        messages.error(self.request, 'Hubo un error al actualizar el cliente.')
        return super().form_invalid(form)


# Clase para listar reservas
class BookingView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Reserva
    template_name = 'Hotel/reserva.html'
    context_object_name = 'reservas'  # Nombre del contexto

    def test_func(self):
        # Verifica permisos del usuario
        return self.request.user.tipo_usuario in ['ADMINISTRADOR', 'ENCARGADO'] or self.request.user.is_superuser

    def handle_no_permission(self):
        # Página personalizada al no tener permisos
        return render(self.request, 'Hotel/sin_permiso.html', status=403)

    def get_context_data(self, **kwargs):
        # Agrega información adicional al contexto
        context = super().get_context_data(**kwargs)
        context['rooms'] = Habitacion.objects.all()
        context['clients'] = Client.objects.all()
        context['form'] = ReservaForm()

        for reserva in context['reservas']:
            # Formatea el RUT del cliente asociado a la reserva
            rut = ''.join([c for c in reserva.cliente.numero_documento if c.isdigit()])
            if len(rut) == 9:
                reserva.cliente.formatted_numero_documento = f'{rut[:2]}.{rut[2:5]}.{rut[5:8]}-{rut[8]}'
            else:
                reserva.cliente.formatted_numero_documento = reserva.cliente.numero_documento

            # Actualiza las fechas para estados cancelados o check-out
            if reserva.estado_reserva in ['CANCELADA', 'CHECK-OUT']:
                reserva.FechaEntrada = reserva.original_FechaEntrada
                reserva.FechaSalida = reserva.original_FechaSalida

        for cliente in context['clients']:
            # Formatea el RUT de los clientes
            rut = ''.join([c for c in cliente.numero_documento if c.isdigit()])
            if len(rut) == 9:
                cliente.formatted_numero_documento = f'{rut[:2]}.{rut[2:5]}.{rut[5:8]}-{rut[8]}'
            else:
                cliente.formatted_numero_documento = cliente.numero_documento

        return context


# Clase para cambiar el estado de reservas
class CambiarEstadoRev(View):
    def post(self, request, codigo_reserva):
        # Cambia el estado de la reserva y actualiza habitaciones asociadas
        reserva = get_object_or_404(Reserva, codigo_reserva=codigo_reserva)

        if reserva.estado_reserva == 'CONFIRMADA':
            for habitacion in reserva.habitaciones.all():
                habitacion.estado_habitacion = 'LIMPIEZA'
                habitacion.save()

            reserva.estado_reserva = 'CHECK-OUT'
            reserva.save()

            messages.success(
                self.request,
                f'Las habitaciones asociadas a la reserva R{reserva.codigo_reserva} se actualizaron a estado de limpieza.'
            )

        return redirect('reserva')


class BookingViewCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Reserva
    form_class = ReservaForm

    def test_func(self):
        # Permite acceso solo a usuarios con roles específicos (ADMINISTRADOR, ENCARGADO o superusuario)
        return self.request.user.tipo_usuario in ['ADMINISTRADOR', 'ENCARGADO'] or self.request.user.is_superuser

    def handle_no_permission(self):
        # Muestra una página personalizada de error de permisos
        return render(self.request, 'Hotel/sin_permiso.html', status=403)

    def form_valid(self, form):
        # Asigna el usuario actual a la reserva y la guarda
        instance = form.save(commit=False)
        instance.usuario = self.request.user
        instance.save()

        # Asocia las habitaciones seleccionadas con la reserva
        habitaciones = form.cleaned_data['habitaciones']
        instance.habitaciones.set(habitaciones)

        # Devuelve una respuesta en formato JSON indicando éxito
        return JsonResponse({'success': True, 'message': 'Reserva creada correctamente!'})

    def form_invalid(self, form):
        # Devuelve una respuesta JSON con los errores de validación del formulario
        return JsonResponse({'success': False, 'errors': form.errors})



class BookingViewDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Reserva
    success_url = reverse_lazy('reserva')

    def test_func(self):
        # Permite acceso solo a usuarios autorizados
        return self.request.user.tipo_usuario in ['ADMINISTRADOR', 'ENCARGADO'] or self.request.user.is_superuser

    def handle_no_permission(self):
        # Redirige a una página de error de permisos si el usuario no está autorizado
        return render(self.request, 'Hotel/sin_permiso.html', status=403)

    def form_valid(self, form):
        # Lógica personalizada para manejar acciones antes de eliminar
        codigo_reserva = self.get_object().codigo_reserva
        return super().form_valid(form)

    
class BookingViewUpdate(LoginRequiredMixin, UpdateView):
    model = Reserva
    fields = ['FechaEntrada', 'FechaSalida', 'estado_reserva', 'detallesRev']
    template_name = 'Hotel/Reserva/reserva_update.html'
    success_url = reverse_lazy('reserva')

    def test_func(self):
        # Verifica permisos para actualizar la reserva
        return self.request.user.tipo_usuario in ['ADMINISTRADOR', 'ENCARGADO'] or self.request.user.is_superuser

    def handle_no_permission(self):
        # Muestra una página de error si no tiene permisos
        return render(self.request, 'Hotel/sin_permiso.html', status=403)

    def form_valid(self, form):
        # Actualiza la reserva y cambia el estado de las habitaciones según sea necesario
        reserva = form.save(commit=False)
        reserva.save()

        if reserva.estado_reserva == 'CANCELADA':
            Habitacion.objects.filter(id__in=[h.id for h in reserva.habitaciones.all()]).update(estado_habitacion='DISPONIBLE')
        elif reserva.estado_reserva == 'CHECK-OUT':
            Habitacion.objects.filter(id__in=[h.id for h in reserva.habitaciones.all()]).update(estado_habitacion='LIMPIEZA')

        return super().form_valid(form)

    def get_form(self, *args, **kwargs):
        # Configura widgets y validaciones para los campos del formulario
        form = super().get_form(*args, **kwargs)

        form.fields['FechaEntrada'].widget.attrs.update({
            'class': 'form-control',
            'type': 'date',
            'min': datetime.now().strftime('%Y-%m-%d')
        })
        form.fields['FechaSalida'].widget.attrs.update({
            'class': 'form-control',
            'type': 'date',
            'min': datetime.now().strftime('%Y-%m-%d')
        })
        form.fields['estado_reserva'].choices = [
            choice for choice in form.fields['estado_reserva'].choices if choice[0] != 'CHECK-OUT'
        ]
        form.fields['estado_reserva'].widget.attrs.update({'class': 'form-control'})
        form.fields['detallesRev'].widget.attrs.update({'class': 'form-control'})

        return form


#FACTURA

class Factura_pdf(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Reserva
    template_name = 'Hotel/factura.html'
    context_object_name = 'reserva'

    def get(self, request, *args, **kwargs):
        try:
            # Obtiene la reserva basada en el código de factura proporcionado
            codigo_factura = kwargs['codigo_factura']
            reserva = get_object_or_404(Reserva, codigo_factura=codigo_factura)
        except KeyError:
            # Devuelve un error si no se proporciona el código
            return HttpResponse("Código de factura no proporcionado.", status=400)

        # Calcula el total de la estadía y los impuestos
        dias_estadia = (reserva.FechaSalida - reserva.FechaEntrada).days if reserva.FechaEntrada and reserva.FechaSalida else 0
        total = sum(h.precio_habitacion for h in reserva.habitaciones.all()) * dias_estadia
        total_impuestos = total + (total * 0.19)

        reserva.monto_total = total
        reserva.save()

        context = {
            'reserva': reserva,
            'habitaciones': reserva.habitaciones.all(),
            'dias_estadia': dias_estadia,
            'total': total,
            'total_impuestos': total_impuestos,
            'user': request.user
        }

        # Renderiza la plantilla y genera el PDF
        html_string = render_to_string(self.template_name, context)
        html = HTML(string=html_string)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename=factura_{reserva.codigo_factura}.pdf'
        html.write_pdf(target=response)

        return response

    def test_func(self):
        # Verifica permisos para ver la factura
        return self.request.user.tipo_usuario in ['ADMINISTRADOR', 'ENCARGADO'] or self.request.user.is_superuser

    def handle_no_permission(self):
        # Redirige a una página de error de permisos si no tiene acceso
        return render(self.request, 'Hotel/sin_permiso.html', status=403)

    

#REPORTE OCUPACION
def reporte_ocupacion(request):
    # Genera un gráfico para el reporte de ocupación
    imagen = generar_reporte_ocupacion()

    # Codifica la imagen a base64 para enviarla al frontend
    imagen_base64 = base64.b64encode(imagen.getvalue()).decode('utf-8')

    # Renderiza la plantilla con la imagen codificada
    return render(request, 'Hotel/reporte_habitaciones.html', {'imagen_base64': imagen_base64})
