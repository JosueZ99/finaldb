from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template import loader
from django.db import connection
import psycopg2, re

from .models import Clientes, Inventario, Catalogos, Ventas, RegistroVentas
from .forms import IngresarClientesForm, ActualizarClientesForm, IngresarInventarioForm, ActualizarInventarioForm, IngresarCatalogoForm, ActualizarCatalogoForm, IngresarVentaForm

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

def ventas(request):
    ventas = Ventas.objects.all().order_by('id')
    registro_ventas = RegistroVentas.objects.select_related('id_forma_pago', 'id_estado_venta').order_by('id')
    context = {
        'ventas': ventas,
        'registro_ventas': registro_ventas,
    }
    template = loader.get_template('ventas.html')
    return HttpResponse(template.render(context, request))

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

def ingresar_venta(request):
    if request.method == 'POST':
        form = IngresarVentaForm(request.POST)
        if form.is_valid():
            cedula_cliente = form.cleaned_data['cedula_cliente']
            productos_comprados = form.cleaned_data['productos_comprados']
            forma_pago = form.cleaned_data['forma_pago']

            with connection.cursor() as cursor:
                cursor.execute("""
                    CALL ingresar_venta(%s, %s::jsonb, %s)
                """, [cedula_cliente, productos_comprados, forma_pago])
                
            return redirect('videojuegos:ventas')
    else:
        form = IngresarVentaForm()
        
    return render(request, 'ingresar_venta.html', {'form': form})
        
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

def actualizar_catalogo(request, id):
    catalogos = get_object_or_404(Catalogos, id = id)
    
    if request.method == 'POST':
        form = ActualizarCatalogoForm(request.POST, initial={
            'id': catalogos.id,
            'catalogo': catalogos.catalogo,
            'item_catalogo': catalogos.item_catalogo,
        })
        if form.is_valid():
            catalogo = form.cleaned_data['catalogo']
            item_catalogo = form.cleaned_data['item_catalogo']
            
            with connection.cursor() as cursor:
                cursor.execute("""
                    CALL actualizar_catalogo(%s, %s, %s)
                """, [id, catalogo, item_catalogo])
                
            return redirect('videojuegos:catalogos')
    else:
        form = ActualizarCatalogoForm(initial={
            'id': catalogos.id,
            'catalogo': catalogos.catalogo,
            'item_catalogo': catalogos.item_catalogo,
        })
    
    return render(request, 'actualizar_catalogo.html', {'form': form})

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

def consultar_venta(request):
    cedula = request.GET.get('cedula_cliente', '')
    venta_info = []
    mensaje = 'No se encontró ninguna venta'
    try:
        if cedula:
            with connection.cursor() as cursor:
                cursor.execute("CALL consultar_ventas(%s)", [cedula])
                conn = cursor.connection
                conn.poll()
                notices = conn.notices
                
                # Regular expression to match each notice
                notice_pattern = re.compile(
                    r'ID:\s*(\d+)\s*\|\s*Cédula:\s*(\S+)\s*\|\s*Fecha de compra:\s*(\d{4}-\d{2}-\d{2})\s*\|\s*Forma de pago:\s*(.*?)\nProductos Comprados:\n((?:Producto \d+ - ID: \d+, Cantidad: \d+\n?)+)?',
                    re.DOTALL
                )

                for notice in notices:
                    matches = notice_pattern.finditer(notice)

                    for match in matches:
                        productos_comprados = match.group(5)
                        productos = []

                        if productos_comprados:
                            productos_list = productos_comprados.strip().split('\n')
                            for producto in productos_list:
                                prod_match = re.match(
                                    r'Producto (\d+) - ID: (\d+), Cantidad: (\d+)',
                                    producto
                                )
                                if prod_match:
                                    productos.append({
                                        'numero': prod_match.group(1),
                                        'id': prod_match.group(2),
                                        'cantidad': prod_match.group(3),
                                    })

                        venta_info.append({
                            'id': match.group(1),
                            'cedula': match.group(2),
                            'fecha': match.group(3),
                            'forma_pago': match.group(4).strip(),
                            'productos': productos,
                        })
                if not venta_info:
                    mensaje = 'No se encontraron ventas para esta cédula.'
                
    except Exception as e:
        mensaje = str(e)
        
    context = {
        'venta_info': venta_info,
        'mensaje': mensaje,
    } 
    
    return render(request, 'consultar_venta.html', context)


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

    formatos = Catalogos.objects.filter(id_raiz=1)
    generos = Catalogos.objects.filter(id_raiz=4)
    plataformas = Catalogos.objects.filter(id_raiz=11)

    return render(request, 'ingresar_inventario.html', {
        'form': form,
        'formatos': formatos,
        'generos': generos,
        'plataformas': plataformas
    })

def actualizar_inventario(request, codigo_producto):
    inventario = get_object_or_404(Inventario, codigo_producto=codigo_producto)
    
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
        
    return render(request, 'actualizar_inventario.html', {
        'form': form
    })


    
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


def detalles_venta(request, id):
    registro_venta = get_object_or_404(RegistroVentas, id=id)
    venta = registro_venta.id_productos_vendidos
    
    productos = []
    for i in range(1, 6):  # There are up to 5 products
        producto = getattr(venta, f'id_producto_{i}')
        cantidad = getattr(venta, f'cantidad_producto_{i}')
        if producto:
            productos.append({
                'producto': producto,
                'cantidad': cantidad,
            })

    context = {
        'venta': venta,
        'registro_venta': registro_venta,
        'productos': productos,
    }

    return render(request, 'detalles_venta.html', context)