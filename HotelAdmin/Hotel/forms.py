from django import forms
from .models import Tech


class TechForm(forms.ModelForm):
    class Meta:
        model = Tech
        fields = ['name', 'last_name','avatar']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar':forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
