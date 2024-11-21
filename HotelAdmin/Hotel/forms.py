from django import forms
from .models import TipoUsuario,Reserva,Client,Habitacion
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

class ClientForm(forms.ModelForm):
    TIPO_DOCUMENTO = [
        ('RUT', 'RUT')
    ]
    tipo_documento = forms.ChoiceField(
        choices=TIPO_DOCUMENTO,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    telefono= forms.CharField(
        widget = forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'tel'
            }))
        
    class Meta:
        model = Client
        fields = [
            'numero_documento', 
            'tipo_documento',
            'nombre',
            'apellido',
            'telefono',
            'correo'
            ]
        widgets = {
            'numero_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre':forms.TextInput(attrs={'class': 'form-control'}),
            'apellido':forms.TextInput(attrs={'class': 'form-control'}),
            'correo':forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_numero_documento(self):
        numero_documento = self.cleaned_data.get('numero_documento', '').strip()

        rut = ''.join([c for c in numero_documento if c.isdigit()])

        if len(rut) != 9:
            raise forms.ValidationError("El RUT debe tener exactamente 9 dígitos.")

        return rut

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')

        if not telefono.startswith('9'):    
            raise forms.ValidationError("El numero debe empezar con 9")
        
        if len(telefono) != 9:
            raise forms.ValidationError("El numero debe ser de 9 digitos")
        
        return telefono

class RoomForm(forms.ModelForm):
    ESTADO_HABITACION = [
        ('DISPONIBLE', 'Disponible'),
        ('OCUPADA', 'Ocupada'),
        ('LIMPIEZA', 'Limpieza'),
    ]
    TIPO_HABITACION = [
        ('SIMPLE', 'Simple'),
        ('DOBLE', 'Doble'),
        ('SUITE', 'Suite'),
    ]
    tipo_habitacion = forms.ChoiceField(
        choices=TIPO_HABITACION,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    estado_habitacion = forms.ChoiceField(
        choices=ESTADO_HABITACION,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    class Meta:
        model = Habitacion
        fields = ['numero_habitacion', 'tipo_habitacion','estado_habitacion','precio_habitacion']
        widgets  = {
                'numero_habitacion': forms.NumberInput(attrs={'class': 'form-control'}),
                'precio_habitacion': forms.NumberInput(attrs={'class': 'form-control'})
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
        