from django import forms
from .models import Catalogos

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
    nombre = forms.CharField(label='Nombre del Videojuego', max_length=100)
    formato = forms.ChoiceField(label='Formato')
    genero = forms.ChoiceField(label='Género')
    plataforma = forms.ChoiceField(label='Plataforma')
    ano_lanzamiento = forms.IntegerField(label='Año de Lanzamiento')
    precio = forms.DecimalField(label='Precio', max_digits=10, decimal_places=2)
    stock = forms.IntegerField(label='Stock')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        formatos = Catalogos.objects.filter(id_raiz=1).values_list('item_catalogo', 'item_catalogo')
        generos = Catalogos.objects.filter(id_raiz=4).values_list('item_catalogo', 'item_catalogo')
        plataformas = Catalogos.objects.filter(id_raiz=11).values_list('item_catalogo', 'item_catalogo')

        self.fields['formato'].choices = [('', 'Seleccione un formato')] + list(formatos)
        self.fields['genero'].choices = [('', 'Seleccione un género')] + list(generos)
        self.fields['plataforma'].choices = [('', 'Seleccione una plataforma')] + list(plataformas)
    
class ActualizarInventarioForm(forms.Form):
    codigo_producto = forms.CharField(widget=forms.HiddenInput(), label='Código del Producto', max_length=10)
    nombre = forms.CharField(label='Nombre del videojuego', max_length=100)
    formato = forms.ChoiceField(label='Formato')
    genero = forms.ChoiceField(label='Género')
    plataforma = forms.ChoiceField(label='Plataforma')
    ano_lanzamiento = forms.IntegerField(label='Año de Lanzamiento')
    precio = forms.FloatField(label='Precio')
    stock = forms.IntegerField(label='Stock')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        formatos = Catalogos.objects.filter(id_raiz=1).values_list('item_catalogo', 'item_catalogo')
        generos = Catalogos.objects.filter(id_raiz=4).values_list('item_catalogo', 'item_catalogo')
        plataformas = Catalogos.objects.filter(id_raiz=11).values_list('item_catalogo', 'item_catalogo')

        self.fields['formato'].choices = [('', 'Seleccione un formato')] + list(formatos)
        self.fields['genero'].choices = [('', 'Seleccione un género')] + list(generos)
        self.fields['plataforma'].choices = [('', 'Seleccione una plataforma')] + list(plataformas)

    
class IngresarCatalogoForm(forms.Form):
    catalogo = forms.CharField(label='Catalogo', max_length=100)
    item_catalogo = forms.CharField(label='Item Catalogo', max_length=100)
    
class ActualizarCatalogoForm(forms.Form):
    id = forms.IntegerField(label='ID')
    catalogo = forms.CharField(label='Catalogo', max_length=100)
    item_catalogo = forms.CharField(label='Item Catalogo', max_length=100)
    
class IngresarVentaForm(forms.Form):
    cedula_cliente = forms.CharField(label='Cédula del Cliente', max_length=10)
    productos_comprados = forms.CharField(label='Productos Comprados (formato: [{"id_producto": 1, "cantidad": 2}, ...])')
    forma_pago = forms.ChoiceField(label='Forma de Pago')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        formas_pago = Catalogos.objects.filter(id_raiz=21).values_list('item_catalogo', 'item_catalogo') 
        self.fields['forma_pago'].choices = [('', 'Seleccione una forma de pago')] + list(formas_pago)