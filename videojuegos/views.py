from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template import loader
from django.db import connection
import psycopg2, re

from .models import Clientes, Inventario, Catalogos
from .forms import IngresarClientesForm, ActualizarClientesForm, IngresarInventarioForm, ActualizarInventarioForm, IngresarCatalogoForm, ActualizarCatalogoForm

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

def catalogos(request):
    catalogos = Catalogos.objects.order_by('id')
    template = loader.get_template('catalogos.html')
    return HttpResponse(template.render({'catalogos': catalogos}, request))

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

def consultar_cliente(request):
    cedula = request.GET.get('cedula', '')
    cliente_info = None
    mensaje = 'No se encontró ningún cliente'
    try:
        if cedula:
            with connection.cursor() as cursor:
                cursor.execute("CALL consultar_cliente(%s)", [cedula])
                conn = cursor.connection
                conn.poll()
                notices = conn.notices
                
                cliente_info = {}
                for notice in notices:
                    match = re.match(
                        r"NOTICE:  ID: (\d+), Cédula: (\S+), Apellidos y Nombres: (.+?), Correo: (.+?), Provincia: (.+?), Dirección: (.+?), Estado Cliente: (.+?), Teléfono: ([\d\s\+\-]+)",
                        notice
                    )
                    if match:
                        cliente_info = {
                            'id': match.group(1),
                            'cedula': match.group(2),
                            'apellidos_nombres': match.group(3),
                            'correo': match.group(4),
                            'provincia': match.group(5),
                            'direccion': match.group(6),
                            'estado': match.group(7),
                            'telefono': match.group(8),
                        }
                    else:
                        mensaje = notice
    except Exception as e:
        mensaje = str(e)
        
    context = {
        'cliente_info': cliente_info,
        'mensaje': mensaje,
    }

    return render(request, 'consultar_cliente.html', context)


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

def consultar_inventario(request):
    codigo_producto = request.GET.get('codigo_producto', '')
    inventario_info = None
    mensaje = 'No se encontró ningún producto en el inventario'
    try:
        if codigo_producto:
            with connection.cursor() as cursor:
                cursor.execute("CALL consultar_inventario(%s)", [codigo_producto])
                conn = cursor.connection
                conn.poll()
                notices = conn.notices
                
                inventario_info = {}
                for notice in notices:
                    match = re.match(
                        r"NOTICE:  ID: (\d+), Código de Producto: (\S+), Nombre: (.+?), Formato: (.+?), Género: (.+?), Plataforma: (.+?), Año de Lanzamiento: (\d+), Precio: (\d+\.\d+), Stock: (\d+), Estado de Producto: (.+)",
                        notice
                    )
                    if match:
                        inventario_info = {
                            'id': match.group(1),
                            'codigo_producto': match.group(2),
                            'nombre': match.group(3),
                            'formato': match.group(4),
                            'genero': match.group(5),
                            'plataforma': match.group(6),
                            'ano_lanzamiento': match.group(7),
                            'precio': match.group(8),
                            'stock': match.group(9),
                            'estado': match.group(10),
                        }
                    else:
                        mensaje = notice
    except Exception as e:
        mensaje = str(e)
        
    context = {
        'inventario_info': inventario_info,
        'mensaje': mensaje,
    }

    return render(request, 'consultar_inventario.html', context)
def ingresar_catalogo(request):
    if request.method == 'POST':
        form = IngresarCatalogoForm(request.POST)
        if form.is_valid():
            catalogo = form.cleaned_data['catalogo']
            item_catalogo = form.cleaned_data['item_catalogo']

            with connection.cursor() as cursor:
                cursor.execute("""
                    CALL ingresar_catalogo(%s, %s)
                """, [catalogo, item_catalogo])
                
            return redirect('videojuegos:catalogos')
    else:
        form = IngresarCatalogoForm()
        
    return render(request, 'ingresar_catalogo.html', {'form': form})

def actualizar_catalogo(request, id):
    catalogo = get_object_or_404(Catalogos, id = id)
    
    if request.method == 'POST':
        form = ActualizarCatalogoForm(request.POST, initial={
            'id': catalogo.id,
            'catalogo': catalogo.catalogo,
            'item_catalogo': catalogo.item_catalogo,
        })
        if form.is_valid():
            catalogo = form.cleaned_data['catalogo']
            item_catalogo = form.cleaned_data['item_catalogo']
            
            with connection.cursor() as cursor:
                cursor.execute("""
                    CALL actualizar_catalogo(%s, %s)
                """, [id, catalogo, item_catalogo])
                
            return redirect('videojuegos:catalogos')
    else:
        form = ActualizarCatalogoForm(initial={
            'id': catalogo.id,
            'catalogo': catalogo.catalogo,
            'item_catalogo': catalogo.item_catalogo,
        })
    
    return render(request, 'actualizar_catalogo.html', {'form': form})
