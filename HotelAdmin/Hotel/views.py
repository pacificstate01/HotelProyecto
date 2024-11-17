from django.views.generic import ListView,DetailView,CreateView, UpdateView, DeleteView,TemplateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TipoUsuario,Reserva
from .forms import ReservaForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404,JsonResponse


class HomeView(LoginRequiredMixin,TemplateView):
    template_name = 'Hotel/dashboard.html'

class ClientsView(TemplateView):
    template_name = 'Hotel/reporte_clientes.html'

class ManageClientsView(TemplateView):
    template_name = 'Hotel/gestion_clientes.html'

class ManageRoomsView(TemplateView):
    template_name = 'Hotel/gestion_habitaciones.html'

class BookingView(TemplateView):
    template_name = 'Hotel/reserva.html'
    def get_context_data(self, **kwargs):
        # Add the form to the context
        context = super().get_context_data(**kwargs)
        context['form'] = ReservaForm()
        return context

