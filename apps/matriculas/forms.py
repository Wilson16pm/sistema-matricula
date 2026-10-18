from django import forms
from .models import Estudiante


class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['dni', 'nombres', 'apellidos', 'fecha_nacimiento',
                  'sexo', 'direccion', 'telefono', 'colegio_procedencia']
        widgets = {
            'dni': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '8'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'colegio_procedencia': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'dni': 'DNI',
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'sexo': 'Sexo',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'colegio_procedencia': 'Colegio de Procedencia',
        }

from .models import Apoderado

class ApoderadoForm(forms.ModelForm):
    class Meta:
        model = Apoderado
        fields = ['dni', 'nombres', 'apellidos', 'parentesco',
                  'telefono', 'direccion', 'email']
        widgets = {
            'dni': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '8'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'parentesco': forms.Select(attrs={'class': 'form-select'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

from .models import Matricula

class MatriculaForm(forms.ModelForm):
    class Meta:
        model = Matricula
        fields = ['estudiante', 'apoderado', 'anio', 'grado_solicitado', 'observaciones']
        widgets = {
            'estudiante': forms.Select(attrs={'class': 'form-select'}),
            'apoderado': forms.Select(attrs={'class': 'form-select'}),
            'anio': forms.Select(attrs={'class': 'form-select'}),
            'grado_solicitado': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
from .models import Pago

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['matricula', 'monto', 'metodo', 'numero_operacion', 'observacion']
        widgets = {
            'matricula': forms.Select(attrs={'class': 'form-select'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'metodo': forms.Select(attrs={'class': 'form-select'}),
            'numero_operacion': forms.TextInput(attrs={'class': 'form-control'}),
            'observacion': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'numero_operacion': 'N° Operación / Recibo',
        }

