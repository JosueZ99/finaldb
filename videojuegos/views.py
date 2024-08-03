from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.db import connection

from .models import Clientes
from .forms import IngresarClientesForm, ActualizarClientesForm

# Create your views here.
def index(request):
    clientes = Clientes.objects.order_by('apellidos_nombres')
    template = loader.get_template('index.html')
    return HttpResponse(template.render({'clientes': clientes}, request))

def clientes(request):
    clientes = Clientes.objects.order_by('id')
    template = loader.get_template('clientes.html')
    return HttpResponse(template.render({'clientes': clientes}, request))

def ingresar_cliente(request):
    if request.method == 'POST':
        form = IngresarClientesForm(request.POST)
        if form.is_valid():
            apellidos_nombres = form.cleaned_data['apellidos_nombres']
            cedula = form.cleaned_data['cedula']
            correo = form.cleaned_data['correo']
            direccion = form.cleaned_data['direccion']
            telefono = form.cleaned_data['telefono']

            with connection.cursor() as cursor:
                cursor.execute("""
                    CALL ingresar_cliente(%s, %s, %s, %s, %s)
                """, [apellidos_nombres, cedula, correo, direccion, telefono])
                
            return redirect('videojuegos:clientes')
    else:
        form = IngresarClientesForm()
        
    return render(request, 'ingresar_cliente.html', {'form': form})
        
def actualizar_cliente(request):
    if request.method == 'POST':
        form = ActualizarClientesForm(request.POST)
        if form.is_valid():
            cedula = form.cleaned_data['cedula']
            apellidos_nombres = form.cleaned_data['apellidos_nombres']
            correo = form.cleaned_data['correo']
            direccion = form.cleaned_data['direccion']
            telefono = form.cleaned_data['telefono']
            
            with connection.cursor() as cursor:
                cursor.execute("""
                    CALL actualizar_cliente(%s, %s, %s, %s, %s)
                """, [cedula, apellidos_nombres, correo, direccion, telefono])
                
            return redirect('videojuegos:clientes')
    else:
        form = ActualizarClientesForm()
        
    return render(request, 'actualizar_cliente.html', {'form': form})