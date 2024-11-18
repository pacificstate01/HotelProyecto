from django.views.generic import ListView,DetailView,CreateView, UpdateView, DeleteView,TemplateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TipoUsuario,Reserva,Client
from .forms import ReservaForm,ClientForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404,JsonResponse


class HomeView(LoginRequiredMixin,TemplateView):
    template_name = 'Hotel/dashboard.html'

class ClientsView(TemplateView):
    template_name = 'Hotel/reporte_clientes.html'


class ManageRoomsView(TemplateView):
    template_name = 'Hotel/gestion_habitaciones.html'

#VISTAS CLIENTES
class ManageClientsView(ListView):
    model = Client
    template_name = 'Hotel/gestion_clientes.html'
    context_object_name = 'clients'
    
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
        return JsonResponse({'success': True, 'message': 'Cliente agregado exitosamente!'})

class ClientDelete(DeleteView):
    model = Client
    success_url = reverse_lazy('gestion_cli')

class ClientUpdate(UpdateView):
    model = Client
    form_class = ClientForm
    fields = [
        'numero_documento', 
        'tipo_documento',
        'nombre',
        'apellido',
        'telefono',
        'correo'
    ]
    success_url = reverse_lazy('gestion_cli')
    def form_valid(self, form):
        return super().form_valid(form)

#VISTAS RESERVA
class BookingView(TemplateView):
    template_name = 'Hotel/reserva.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReservaForm()
        return context

