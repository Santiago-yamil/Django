from django import forms
from .models import Solicitud, Apoyo

# Definimos el formulario basado en el Modelo Solicitud
class SolicitudForm(forms.ModelForm):
    # Sobrescribimos el campo apoyo para usar Select en lugar de Input
    # queryset=Apoyo.objects.all() asegura que cargue los apoyos de la DB remota
    apoyo = forms.ModelChoiceField(
        queryset=Apoyo.objects.all(), 
        empty_label="--- Seleccione un Apoyo ---",
        widget=forms.Select(attrs={'class': 'border rounded p-2 w-full'})
    )

    class Meta:
        model = Solicitud
        fields = [
            'curp', 
            'nombre', 
            'primer_apellido', 
            'segundo_apellido', 
            'genero', 
            'descripcion',
            'apoyo', # Usaremos el campo sobrescrito arriba
            # Omitimos fields como estado y fecha_registro que son automáticos
        ]
        
        # Añadir estilos a todos los campos de entrada
        widgets = {
            'curp': forms.TextInput(attrs={'class': 'border rounded p-2 w-full'}),
            'nombre': forms.TextInput(attrs={'class': 'border rounded p-2 w-full'}),
            'primer_apellido': forms.TextInput(attrs={'class': 'border rounded p-2 w-full'}),
            'segundo_apellido': forms.TextInput(attrs={'class': 'border rounded p-2 w-full'}),
            'genero': forms.TextInput(attrs={'class': 'border rounded p-2 w-full'}),
            'descripcion': forms.Textarea(attrs={'class': 'border rounded p-2 w-full', 'rows': 4}),
        }