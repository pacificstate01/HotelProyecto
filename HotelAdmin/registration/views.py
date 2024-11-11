from django.views.generic.edit import CreateView,UpdateView
from django.urls import reverse_lazy
from Hotel.models import Tech
from Hotel.forms import TechForm
from django.contrib.auth.forms import UserCreationForm
from django import forms


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/Sign_up.html'


    def get_success_url(self):
        return reverse_lazy('login')

    def get_form(self,form_class=None):
        form = super(SignUpView,self).get_form()

        form.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

        return form


class ProfileUpdate(UpdateView):
    form_class = TechForm
    success_url = reverse_lazy('profile')
    template_name= 'registration/Profile_form.html'
    
    def get_object(self):
        profile,created = Tech.objects.get_or_create(user = self.request.user)
        return profile
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_name'] = self.request.user.get_full_name() or self.request.user.username
        return context
