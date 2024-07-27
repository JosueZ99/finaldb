from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.db import connection

from .models import Clientes
from .forms import ClientesForm

# Create your views here.
def index(request):
    clientes = Clientes.objects.order_by('apellidos_nombres')
    template = loader.get_template('index.html')
    return HttpResponse(template.render({'clientes': clientes}, request))

def ingresar_o_actualizar_cliente(request):
    if request.method == 'POST':
        form = ClientesForm(request.POST)
        if form.is_valid():
            apellidos_nombres = form.cleaned_data['apellidos_nombres']
            cedula = form.cleaned_data['cedula']
            correo = form.cleaned_data['correo']
            direccion = form.cleaned_data['direccion']
            telefono = form.cleaned_data['telefono']

            with connection.cursor() as cursor:
                cursor.execute("""
                    CALL ingresar_o_actualizar_cliente(%s, %s, %s, %s, %s)
                """, [apellidos_nombres, cedula, correo, direccion, telefono])
                
            return redirect('videojuegos:index')
    else:
        form = ClientesForm()
    
    return render(request, 'ingresar_o_actualizar_cliente.html', {'form':form})