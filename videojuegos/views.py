from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template import loader
from django.db import connection

from .models import Clientes, Inventario
from .forms import IngresarClientesForm, ActualizarClientesForm, IngresarInventarioForm, ActualizarInventarioForm

# Create your views here.
def index(request):
    clientes = Clientes.objects.order_by('apellidos_nombres')
    template = loader.get_template('index.html')
    return HttpResponse(template.render({'clientes': clientes}, request))

def clientes(request):
    clientes = Clientes.objects.order_by('id')
    template = loader.get_template('clientes.html')
    return HttpResponse(template.render({'clientes': clientes}, request))

def inventario(request):
    inventario = Inventario.objects.order_by('id')
    template = loader.get_template('inventario.html')
    return HttpResponse(template.render({'inventario': inventario}, request))

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
        
def actualizar_cliente(request, cedula):
    cliente = get_object_or_404(Clientes, cedula=cedula)
    
    if request.method == 'POST':
        form = ActualizarClientesForm(request.POST, initial={
            'cedula': cliente.cedula,
            'apellidos_nombres': cliente.apellidos_nombres,
            'correo': cliente.correo,
            'direccion': cliente.direccion,
            'telefono': cliente.telefono,
        })
        if form.is_valid():
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
        form = ActualizarClientesForm(initial={
            'cedula': cliente.cedula,
            'apellidos_nombres': cliente.apellidos_nombres,
            'correo': cliente.correo,
            'direccion': cliente.direccion,
            'telefono': cliente.telefono,
        })
        
    return render(request, 'actualizar_cliente.html', {'form': form})

def ingresar_inventario(request):
    if request.method == 'POST':
        form = IngresarInventarioForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            formato = form.cleaned_data['formato']
            genero = form.cleaned_data['genero']
            plataforma = form.cleaned_data['plataforma']
            ano_lanzamiento = form.cleaned_data['ano_lanzamiento']
            precio = form.cleaned_data['precio']
            stock = form.cleaned_data['stock']

            with connection.cursor() as cursor:
                cursor.execute("""
                    CALL ingresar_inventario(%s, %s, %s, %s, %s, %s, %s)
                """, [nombre, formato, genero, plataforma, ano_lanzamiento, precio, stock])
                
            return redirect('videojuegos:inventario')
    else:
        form = IngresarInventarioForm()
        
    return render(request, 'ingresar_inventario.html', {'form': form})

def actualizar_inventario(request, codigo_producto):
    inventario = get_object_or_404(Inventario, codigo_producto = codigo_producto)
    
    if request.method == 'POST':
        form = ActualizarInventarioForm(request.POST, initial={
            'codigo_producto': inventario.codigo_producto,
            'nombre': inventario.nombre,
            'formato': inventario.id_formato,
            'genero': inventario.id_genero,
            'plataforma': inventario.id_plataforma,
            'ano_lanzamiento': inventario.ano_lanzamiento,
            'precio': inventario.precio,
            'stock': inventario.stock,
        })
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            formato = form.cleaned_data['formato']
            genero = form.cleaned_data['genero']
            plataforma = form.cleaned_data['plataforma']
            ano_lanzamiento = form.cleaned_data['ano_lanzamiento']
            precio = form.cleaned_data['precio']
            stock = form.cleaned_data['stock']
            
            with connection.cursor() as cursor:
                cursor.execute("""
                    CALL actualizar_inventario(%s, %s, %s, %s, %s, %s, %s, %s)
                """, [codigo_producto, nombre, formato, genero, plataforma, ano_lanzamiento, precio, stock])
                
            return redirect('videojuegos:inventario')
    else:
        form = ActualizarInventarioForm(initial={
            'codigo_producto': inventario.codigo_producto,
            'nombre': inventario.nombre,
            'formato': inventario.id_formato,
            'genero': inventario.id_genero,
            'plataforma': inventario.id_plataforma,
            'ano_lanzamiento': inventario.ano_lanzamiento,
            'precio': inventario.precio,
            'stock': inventario.stock,
        })
    
    return render(request, 'actualizar_inventario.html', {'form': form})