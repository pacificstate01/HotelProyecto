from django.views.generic.edit import CreateView,UpdateView
from django.urls import reverse_lazy
from Hotel.models import TipoUsuario
from Hotel.forms import UserForm
from .forms import UserFormReg
from django import forms
from django.contrib import messages

class SignUpView(CreateView):
    form_class = UserFormReg  
    template_name = 'registration/Sign_up.html'

    def get_success_url(self):
        messages.success(self.request, "La cuenta ha sido creada exitosamente.")
        return reverse_lazy('signup')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        form.fields['tipo_usuario'].widget.attrs['class'] = 'form-control'  

        return form


class ProfileUpdate(UpdateView):
    form_class = UserForm
    success_url = reverse_lazy('profile')
    template_name= 'registration/Profile_form.html'
    
    def get_object(self):
        return self.request.user
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_name'] = self.request.user.get_full_name() or self.request.user.username
        return context
