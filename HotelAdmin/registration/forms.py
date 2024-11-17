from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from Hotel.models import TipoUsuario

class UserFormReg(UserCreationForm):
    TIPO_USUARIO = [
         ('', 'Seleccione un tipo de usuario'),
        ('ADMINISTRADOR', 'Administrador de Hotel'),
        ('ENCARGADO', 'Encargado de Hotel'),
        ('AUXILIAR', 'Auxiliar de Aseo'),
    ]
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    tipo_usuario = forms.ChoiceField(
        choices=TIPO_USUARIO,
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )

    class Meta:
        model = TipoUsuario
        fields = ('name', 'last_name', 'username', 'password1', 'password2', 'tipo_usuario')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden. Intente nuevamente.")

        try:
            
            validate_password(password1)  
        except ValidationError as e:
            for msg in e.messages:
                if msg == 'This password is too similar to your other personal information.':
                    raise forms.ValidationError("La contraseña es muy similar a otra informacion personal.")
                elif msg == 'This password is too short. It must contain at least 8 characters.':
                    raise forms.ValidationError("La contraseña debe contener al menos 8 caracteres.")
                elif msg == 'This password is too common.':
                    raise forms.ValidationError("La contraseña no debe ser comun.")
                elif msg == 'This password is entirely numeric.':
                    raise forms.ValidationError("La contraseña no debe ser completamente numerica.")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo_usuario = self.cleaned_data['tipo_usuario']
        if commit:
            user.save()
        return user
