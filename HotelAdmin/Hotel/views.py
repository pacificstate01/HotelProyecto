from django.views.generic import ListView,DetailView,CreateView, UpdateView, DeleteView,TemplateView
from django.views.generic.edit import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import TipoUsuario,Reserva,Client,Habitacion
from .forms import ReservaForm,ClientForm,RoomForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404,JsonResponse,HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404,redirect,render
from django.contrib import messages
from django.core.exceptions import ValidationError
from datetime import datetime
from django.utils import timezone
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
from datetime import timedelta

#VISTA REPORTES Y MENU PRINCIPAL
class HomeView(LoginRequiredMixin,TemplateView):
    template_name = 'Hotel/dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pendiente'] = Reserva.objects.filter(estado_reserva='PENDIENTE').count()
        context['disponible'] = Habitacion.objects.filter(estado_habitacion='DISPONIBLE').count()
        context['ocupado'] = Habitacion.objects.filter(estado_habitacion='OCUPADA').count()
        context['limpieza'] = Habitacion.objects.filter(estado_habitacion='LIMPIEZA').count()
        context['total'] = (Habitacion.objects.filter(estado_habitacion='DISPONIBLE').count() + 
        Habitacion.objects.filter(estado_habitacion='OCUPADA').count() + Habitacion.objects.filter(estado_habitacion='LIMPIEZA').count())
        return context
class ClientsView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Reserva
    template_name = 'Hotel/reporte_clientes.html'
    context_object_name = 'clients'

    def test_func(self):
        return self.request.user.tipo_usuario == 'ADMINISTRADOR' or self.request.user.tipo_usuario == 'ENCARGADO' or self.request.user.is_superuser   

    def handle_no_permission(self):
        return render(self.request, 'Hotel/sin_permiso.html', status=403)

class ReporteHabitaciones(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Reserva
    template_name = 'Hotel/reporte_habitaciones.html'
    context_object_name = 'habitaciones'

    def test_func(self):
        return self.request.user.tipo_usuario == 'ADMINISTRADOR' or self.request.user.tipo_usuario == 'ENCARGADO' or self.request.user.is_superuser   

    def handle_no_permission(self):
        return render(self.request, 'Hotel/sin_permiso.html', status=403)

#VISTAS HABITACIONES

class ManageRoomsView(LoginRequiredMixin,ListView):
    model = Habitacion
    template_name = 'Hotel/gestion_habitaciones.html'
    context_object_name = 'rooms'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RoomForm()
        return context

class ManageRoomCreate(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Habitacion
    form_class = RoomForm
    def test_func(self):
        return self.request.user.tipo_usuario == 'ADMINISTRADOR' or self.request.user.tipo_usuario == 'ENCARGADO' or self.request.user.is_superuser   

    def handle_no_permission(self):
        return render(self.request, 'Hotel/sin_permiso.html', status=403)
    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({'success': True, 'message': 'Habitacion creada correctamente!'})

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors})

class ManageRoomDelete(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Habitacion
    success_url = reverse_lazy('gestion_hab')
    def test_func(self):
        return self.request.user.tipo_usuario == 'ADMINISTRADOR' or self.request.user.tipo_usuario == 'ENCARGADO' or self.request.user.is_superuser   

    def handle_no_permission(self):
        return render(self.request, 'Hotel/sin_permiso.html', status=403)
    def get_object(self, queryset=None):
        room = super().get_object(queryset)
        
        if room.estado_habitacion == 'OCUPADA':
            self.room_error = 'Habitacion ocupada, no se puede eliminar.'
            return None
        
        return room

    def delete(self, request, *args, **kwargs):
        room = self.get_object()

        if room is None:  
            return JsonResponse({'error': self.room_error}, status=403)
        
        return super().delete(request, *args, **kwargs)

    

class ManageRoomUpdate(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Habitacion
    fields = ['tipo_habitacion', 'precio_habitacion']
    template_name = 'Hotel/Habitaciones/room_update.html'
    def test_func(self):
        return self.request.user.tipo_usuario == 'ADMINISTRADOR' or self.request.user.tipo_usuario == 'ENCARGADO' or self.request.user.is_superuser    

    def handle_no_permission(self):
        return render(self.request, 'Hotel/sin_permiso.html', status=403)
    success_url = reverse_lazy('gestion_hab')
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        form.fields['tipo_habitacion'].widget.attrs.update({'class': 'form-control'})
        form.fields['precio_habitacion'].widget.attrs.update({'class': 'form-control'})
        return form


class CambiarEstadoHab(View):
    def post(self, request, numero_habitacion):
        habitacion = get_object_or_404(Habitacion, numero_habitacion=numero_habitacion)
        if habitacion.estado_habitacion == 'LIMPIEZA':
            habitacion.estado_habitacion = 'DISPONIBLE'
            habitacion.save()
            messages.success(self.request, f'Habitacion numero {habitacion.numero_habitacion} actualizada.')

        return redirect('gestion_hab')

#VISTAS CLIENTES
class ManageClientsView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Client
    template_name = 'Hotel/gestion_clientes.html'
    context_object_name = 'clients'
    def test_func(self):
        return self.request.user.tipo_usuario == 'ADMINISTRADOR' or self.request.user.tipo_usuario == 'ENCARGADO' or self.request.user.is_superuser    

    def handle_no_permission(self):
        return render(self.request, 'Hotel/sin_permiso.html', status=403)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for client in context['clients']:
            rut = ''.join([c for c in client.numero_documento if c.isdigit()])
            if len(rut) == 9:
                client.formatted_numero_documento = f'{rut[:2]}.{rut[2:5]}.{rut[5:8]}-{rut[8]}'
            else:
                client.formatted_numero_documento = client.numero_documento  
        return context

class ClientCreate(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'Hotel/create_client.html'
    success_url = reverse_lazy('gestion_cli')
    def test_func(self):
        return self.request.user.tipo_usuario == 'ADMINISTRADOR' or self.request.user.tipo_usuario == 'ENCARGADO' or self.request.user.is_superuser    

    def handle_no_permission(self):
        return render(self.request, 'Hotel/sin_permiso.html', status=403)
    def form_invalid(self, form):
        errors = {field: error.get_json_data() for field, error in form.errors.items()}
        return JsonResponse({'success': False, 'errors': errors}, status=400)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Cliente con numero de documento {form.instance.numero_documento} ha sido creado correctamente.')
        return JsonResponse({'success': True, 'message': 'Cliente agregado exitosamente!'})

class ClientDelete(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Client
    success_url = reverse_lazy('gestion_cli')
    template_name = None 
    def test_func(self):
        return self.request.user.tipo_usuario == 'ADMINISTRADOR' or self.request.user.tipo_usuario == 'ENCARGADO' or self.request.user.is_superuser   

    def handle_no_permission(self):
        return render(self.request, 'Hotel/sin_permiso.html', status=403)
    def get_object(self, queryset=None):
        numero_documento = self.kwargs.get('numero_documento')
        return Client.objects.get(numero_documento=numero_documento)

    def form_valid(self, form):
        numero_documento = self.get_object().numero_documento
        messages.success(self.request, f'Cliente con número de documento {numero_documento} ha sido eliminado correctamente.')
        return super().form_valid(form)
    
    
class ClientUpdate(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Client
    fields=['nombre', 'apellido', 'telefono', 'correo']
    template_name = 'Hotel/update_client.html'
    success_url = reverse_lazy('gestion_cli')
    def test_func(self):
        return self.request.user.tipo_usuario == 'ADMINISTRADOR' or self.request.user.tipo_usuario == 'ENCARGADO' or self.request.user.is_superuser  

    def handle_no_permission(self):
        return render(self.request, 'Hotel/sin_permiso.html', status=403)
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        form.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        form.fields['apellido'].widget.attrs.update({'class': 'form-control'})
        form.fields['telefono'].widget.attrs.update({'class': 'form-control'})
        form.fields['correo'].widget.attrs.update({'class': 'form-control'})
        telefono_field = form.fields['telefono']
        telefono_field.required = True  
        telefono_field.validators.append(self.validate_telefono)            
        return form

    def validate_telefono(self, value):
        if not value:
            raise ValidationError("El número de teléfono es obligatorio.")
        if not value.startswith('9'):
            raise ValidationError("El número debe empezar con 9.")
        if len(value) != 9:
            raise ValidationError("El número debe tener exactamente 9 dígitos.")
        return value
    def get_object(self, queryset=None):
        return Client.objects.get(numero_documento=self.kwargs['numero_documento'])
        hotel.save()
        return hotel

    def form_valid(self, form):
        messages.success(self.request, 'Cliente actualizado correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al actualizar el cliente.')
        return super().form_invalid(form)
    
    
#VISTAS RESERVA
class BookingView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Reserva
    template_name = 'Hotel/reserva.html'
    context_object_name = 'reservas'
    def test_func(self):
        return self.request.user.tipo_usuario == 'ADMINISTRADOR' or self.request.user.tipo_usuario == 'ENCARGADO' or self.request.user.is_superuser 

    def handle_no_permission(self):
        return render(self.request, 'Hotel/sin_permiso.html', status=403)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = Habitacion.objects.all()
        context['clients'] = Client.objects.all() 
        context['form'] = ReservaForm()

        for reserva in context['reservas']:
            rut = ''.join([c for c in reserva.cliente.numero_documento if c.isdigit()])
            if len(rut) == 9:
                reserva.cliente.formatted_numero_documento = f'{rut[:2]}.{rut[2:5]}.{rut[5:8]}-{rut[8]}'
            else:
                reserva.cliente.formatted_numero_documento = reserva.cliente.numero_documento  
            if reserva.estado_reserva == 'CANCELADA' or reserva.estado_reserva == 'CHECK-OUT':
                reserva.FechaEntrada = reserva.original_FechaEntrada
                reserva.FechaSalida = reserva.original_FechaSalida

        for cliente in context['clients']:
            rut = ''.join([c for c in cliente.numero_documento if c.isdigit()])  
            if len(rut) == 9:
                cliente.formatted_numero_documento = f'{rut[:2]}.{rut[2:5]}.{rut[5:8]}-{rut[8]}'
            else:
                cliente.formatted_numero_documento = cliente.numero_documento  

        return context
class CambiarEstadoRev(View):
    def post(self, request, codigo_reserva):
        reserva = get_object_or_404(Reserva, codigo_reserva=codigo_reserva)
        habitaciones = Habitacion.objects.all()
        if reserva.estado_reserva == 'CONFIRMADA':  
            if reserva.habitaciones:
                reserva.habitaciones.estado_habitacion = 'LIMPIEZA'
                reserva.habitaciones.save()
            reserva.estado_reserva = 'CHECK-OUT'    
            reserva.save()
            messages.success(self.request, f'Habitacion numero {reserva.habitaciones.numero_habitacion} actualizada a estado de limpieza.')

        return redirect('reserva')

class BookingViewCreate(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Reserva
    form_class = ReservaForm
    def test_func(self):
        return self.request.user.tipo_usuario == 'ADMINISTRADOR' or self.request.user.tipo_usuario == 'ENCARGADO' or self.request.user.is_superuser

    def handle_no_permission(self):
        return render(self.request, 'Hotel/sin_permiso.html', status=403)
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.usuario = self.request.user
        instance.save()
        return JsonResponse({'success': True, 'message': 'Reserva creada correctamente!'})


    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors})


class BookingViewDelete(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Reserva
    success_url = reverse_lazy('reserva')
    def test_func(self):
        return self.request.user.tipo_usuario == 'ADMINISTRADOR' or self.request.user.tipo_usuario == 'ENCARGADO'  or self.request.user.is_superuser

    def handle_no_permission(self):
        return render(self.request, 'Hotel/sin_permiso.html', status=403)

    def form_valid(self, form):
        codigo_reserva = self.get_object().codigo_reserva
        return super().form_valid(form)
    
class BookingViewUpdate(LoginRequiredMixin, UpdateView):
    model = Reserva
    fields = ['FechaEntrada', 'FechaSalida', 'estado_reserva','detallesRev']
    template_name = 'Hotel/Reserva/reserva_update.html'
    success_url = reverse_lazy('reserva')
    def test_func(self):
        return self.request.user.tipo_usuario == 'ADMINISTRADOR' or self.request.user.tipo_usuario == 'ENCARGADO' or self.request.user.is_superuser

    def handle_no_permission(self):
        return render(self.request, 'Hotel/sin_permiso.html', status=403)
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        form.fields['FechaEntrada'].widget.attrs.update({
            'class':'form-control',
            'type': 'date',
            'min': datetime.now().strftime('%Y-%m-%d') 
        })
        form.fields['FechaSalida'].widget.attrs.update({
            'class':'form-control',
            'type': 'date',
            'min': datetime.now().strftime('%Y-%m-%d') 
        })
        form.fields['estado_reserva'].choices = [
                choice for choice in form.fields['estado_reserva'].choices if choice[0] != 'CHECK-OUT'
        ]
        form.fields['estado_reserva'].widget.attrs.update({
            'class': 'form-control'
        })
        form.fields['detallesRev'].widget.attrs.update({
            'class': 'form-control'
        })
        return form

#FACTURA


class Factura_pdf(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Reserva
    template_name = 'Hotel/factura.html'
    context_object_name = 'reserva'

    def get(self, request, *args, **kwargs):
        try:
            codigo_factura = kwargs['codigo_factura']
            reserva = get_object_or_404(Reserva, codigo_factura=codigo_factura)
        except KeyError:
            return HttpResponse("Código de factura no proporcionado.", status=400)

       
        habitacion = reserva.habitaciones
        dias_estadia = (reserva.FechaSalida - reserva.FechaEntrada).days
        total = habitacion.precio_habitacion * dias_estadia if habitacion else 0

        
        reserva.monto_total = total
        reserva.save()

        context = {
            'reserva': reserva,
            'habitacion': habitacion,
            'dias_estadia': dias_estadia,
            'total': total,
        }

        html_string = render_to_string(self.template_name, context)
        html = HTML(string=html_string)

   
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename=factura_{reserva.codigo_factura}.pdf'
        html.write_pdf(target=response)

        return response

    def test_func(self):
        return self.request.user.tipo_usuario in ['ADMINISTRADOR', 'ENCARGADO'] or self.request.user.is_superuser

    def handle_no_permission(self):
        return render(self.request, 'Hotel/sin_permiso.html', status=403)