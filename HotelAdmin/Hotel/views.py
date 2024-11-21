from django.views.generic import ListView,DetailView,CreateView, UpdateView, DeleteView,TemplateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TipoUsuario,Reserva,Client,Habitacion
from .forms import ReservaForm,ClientForm,RoomForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404,JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError

class HomeView(LoginRequiredMixin,TemplateView):
    template_name = 'Hotel/dashboard.html'

class ClientsView(TemplateView):
    template_name = 'Hotel/reporte_clientes.html'


class ManageRoomsView(ListView):
    model = Habitacion
    template_name = 'Hotel/gestion_habitaciones.html'
    context_object_name = 'rooms'

class ManageRoomCreate(CreateView):
    model = Habitacion
    form_class = RoomForm
    template_name = 'Hotel/create_room.html'
    success_url = reverse_lazy('gestion_hab')






#VISTAS CLIENTES
class ManageClientsView(ListView):
    model = Client
    template_name = 'Hotel/gestion_clientes.html'
    context_object_name = 'clients'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for client in context['clients']:
            rut = ''.join([c for c in client.numero_documento if c.isdigit()])
            if len(rut) == 9:
                client.formatted_numero_documento = f'{rut[:2]}.{rut[2:5]}.{rut[5:8]}-{rut[8]}'
            else:
                client.formatted_numero_documento = client.numero_documento  
        return context

class ClientCreate(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'Hotel/create_client.html'
    success_url = reverse_lazy('gestion_cli')

    def form_invalid(self, form):
        errors = {field: error.get_json_data() for field, error in form.errors.items()}
        return JsonResponse({'success': False, 'errors': errors}, status=400)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Cliente con numero de documento {form.instance.numero_documento} ha sido creado correctamente.')
        return JsonResponse({'success': True, 'message': 'Cliente agregado exitosamente!'})

class ClientDelete(LoginRequiredMixin,DeleteView):
    model = Client
    success_url = reverse_lazy('gestion_cli')
    template_name = None 

    def get_object(self, queryset=None):
        numero_documento = self.kwargs.get('numero_documento')
        return Client.objects.get(numero_documento=numero_documento)

    def form_valid(self, form):
        numero_documento = self.get_object().numero_documento
        messages.success(self.request, f'Cliente con número de documento {numero_documento} ha sido eliminado correctamente.')
        return super().form_valid(form)
    
    
class ClientUpdate(LoginRequiredMixin, UpdateView):
    model = Client
    fields=['nombre', 'apellido', 'telefono', 'correo']
    template_name = 'Hotel/update_client.html'
    success_url = reverse_lazy('gestion_cli')

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
class BookingView(TemplateView):
    template_name = 'Hotel/reserva.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReservaForm()
        return context

