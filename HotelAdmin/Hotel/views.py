from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.urls import reverse_lazy



class EntrarLoginView(LoginView):
    template_name = 'Hotel/login.html'  
    redirect_authenticated_user = True

class MenuView(TemplateView):
    template_name = 'Hotel/dashboard.html'

class ClientsView(TemplateView):
    template_name = 'Hotel/clientes.html'

class ManageClientsView(TemplateView):
    template_name = 'Hotel/gestion_clientes.html'

class ManageRoomsView(TemplateView):
    template_name = 'Hotel/gestion_habitaciones.html'

class BookingView(TemplateView):
    template_name = 'Hotel/reserva.html'