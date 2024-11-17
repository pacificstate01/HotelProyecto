from django import forms
from .models import TipoUsuario,Reserva
from datetime import datetime

class UserForm(forms.ModelForm):
    class Meta:
        model = TipoUsuario
        fields = ['name', 'last_name','avatar']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar':forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['FechaHoraEntradas', 'FechaSalida']
        widgets = {
            'FechaHoraEntradas':forms.DateTimeInput(attrs={
                'class':'form-control',
                'type': 'datetime-local',
                'min': datetime.now().strftime('%Y-%m-%dT%H:%M')
            }),
            'FechaSalida':forms.DateInput(attrs={
                'class':'form-control',
                'type': 'date',
                'min': datetime.now().strftime('%Y-%m-%d')
            })
        }
        