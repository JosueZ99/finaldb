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
    
class IngresarInventarioForm(forms.Form):
    nombre = forms.CharField(label='Nombre del videojuego', max_length=100)
    formato = forms.CharField(label='Formato', max_length=100)
    genero = forms.CharField(label='Género', max_length=100)
    plataforma = forms.CharField(label='Plataforma', max_length=100)
    ano_lanzamiento = forms.IntegerField(label='Año de Lanzamiento')
    precio = forms.FloatField(label='Precio')
    stock = forms.IntegerField(label='Stock')
    
class ActualizarInventarioForm(forms.Form):
    codigo_producto = forms.CharField(label='Código del Producto', max_length=10)
    nombre = forms.CharField(label='Nombre del videojuego', max_length=100)
    formato = forms.CharField(label='Formato', max_length=100)
    genero = forms.CharField(label='Género', max_length=100)
    plataforma = forms.CharField(label='Plataforma', max_length=100)
    ano_lanzamiento = forms.IntegerField(label='Año de Lanzamiento')
    precio = forms.FloatField(label='Precio')
    stock = forms.IntegerField(label='Stock')