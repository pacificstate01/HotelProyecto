from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.urls import reverse_lazy



class EntrarLoginView(LoginView):
    template_name = 'Hotel/login.html'  
    redirect_authenticated_user = True

class MenuView(TemplateView):
    template_name = 'Hotel/base.html'