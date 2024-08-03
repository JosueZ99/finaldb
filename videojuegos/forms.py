from django import forms

class IngresarClientesForm(forms.Form):
    apellidos_nombres = forms.CharField(label='Apellidos y Nombres', max_length=100)
    cedula = forms.CharField(label='Cédula', max_length=10)
    correo = forms.CharField(label='Correo Electrónico', max_length=100)
    direccion = forms.CharField(label='Dirección', max_length=100)
    telefono = forms.CharField(label='Teléfono', max_length=10)
    
class ActualizarClientesForm(forms.Form):
    cedula = forms.CharField(label='Cédula', max_length=10)
    apellidos_nombres = forms.CharField(label='Apellidos y Nombres', max_length=100)
    correo = forms.CharField(label='Correo Electrónico', max_length=100)
    direccion = forms.CharField(label='Dirección', max_length=100)
    telefono = forms.CharField(label='Teléfono', max_length=10)
