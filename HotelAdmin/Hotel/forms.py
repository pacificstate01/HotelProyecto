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
    ]
    TIPO_HABITACION = [
        ('', 'Seleccione un tipo de habitacion'),
        ('SIMPLE', 'Simple'),
        ('DOBLE', 'Doble'),
        ('SUITE', 'Suite'),
    ]
    tipo_habitacion = forms.ChoiceField(
        choices=TIPO_HABITACION,
        widget=forms.Select(attrs={'class': 'form-select'}),
        error_messages={
            'required': 'Debe seleccionar un tipo de habitacion.',
        }
    )
    estado_habitacion = forms.ChoiceField(
        choices=ESTADO_HABITACION,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    numero_habitacion = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'Debe ingresar el número de la habitación.',
            'invalid': 'El número de la habitación debe ser válido.',
        }
    )
    precio_habitacion = forms.DecimalField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'Debe ingresar el precio de la habitación.',
            'invalid': 'El precio debe ser un número válido.',
        }
    )
    class Meta:
        model = Habitacion
        fields = ['numero_habitacion', 'tipo_habitacion','estado_habitacion','precio_habitacion']



class ReservaForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Cliente",
        to_field_name='numero_documento',
        error_messages={
            'required': 'Debe seleccionar un cliente.',
        }
    )
    habitaciones = forms.ModelMultipleChoiceField(
        queryset=Habitacion.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label="Habitaciones Disponibles",
        error_messages={
            'required': 'Debe seleccionar una o mas habitaciones.',
        }
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar los datos que se muestran en el campo cliente
        self.fields['cliente'].queryset = Client.objects.all()
        self.fields['cliente'].label_from_instance = lambda obj: f"{obj.nombre} {obj.apellido} - ({obj.numero_documento})"

        # Filtrar habitaciones disponibles dinámicamente
        self.fields['habitaciones'].queryset = Habitacion.objects.filter(estado_habitacion='DISPONIBLE')

    def clean_habitaciones(self):
        habitaciones = self.cleaned_data.get('habitaciones')
        if not habitaciones:
            raise forms.ValidationError("Debes seleccionar al menos una habitación.")
        
        # Validación adicional: verificar si las habitaciones están disponibles
        for habitacion in habitaciones:
            if habitacion.estado_habitacion != 'DISPONIBLE':
                raise forms.ValidationError(f"La habitación {habitacion.numero_habitacion} no está disponible.")
        
        return habitaciones


    class Meta:
        model = Reserva
        fields = [
            'FechaEntrada',
            'FechaSalida',
            'habitaciones', 
            'cliente',
            'detallesRev'
        ]
        widgets = {
            'FechaEntrada': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': datetime.now().strftime('%Y-%m-%d')
            }),
            'FechaSalida': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': datetime.now().strftime('%Y-%m-%d')
            }),
            'detallesRev': forms.Textarea(attrs={'class': 'form-control'})
        }
        