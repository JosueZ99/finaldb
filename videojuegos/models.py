from django.db import models

class Catalogos(models.Model):
    catalogo = models.CharField(max_length=30, blank=True, null=True)
    item_catalogo = models.CharField(max_length=30, blank=True, null=True)
    id_raiz = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.item_catalogo or self.catalogo}'

    class Meta:
        db_table = 'catalogos'

class Clientes(models.Model):
    cedula = models.CharField(max_length=10, unique=True)
    apellidos_nombres = models.CharField(max_length=100)
    correo = models.CharField(max_length=100, unique=True)
    provincia = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    id_estado_cliente = models.ForeignKey(Catalogos, on_delete=models.CASCADE, related_name='clientes', db_column='id_estado_cliente')
    telefono = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return f'{self.apellidos_nombres}'
    
    class Meta:
        db_table = 'clientes'

class Inventario(models.Model):
    nombre = models.CharField(max_length=100)
    id_formato = models.ForeignKey(Catalogos, on_delete=models.CASCADE, related_name='formatos', db_column='id_formato')
    id_genero = models.ForeignKey(Catalogos, on_delete=models.CASCADE, related_name='generos', db_column='id_genero')
    id_plataforma = models.ForeignKey(Catalogos, on_delete=models.CASCADE, related_name='plataformas', db_column='id_plataforma')
    ano_lanzamiento = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    id_estado_producto = models.ForeignKey(Catalogos, on_delete=models.CASCADE, related_name='estados_productos', db_column='id_estado_producto')
    codigo_producto = models.CharField(max_length=10)
    
    def __str__(self):
        return f'{self.nombre}'
    
    class Meta:
        db_table = 'inventario'

class Ventas(models.Model):
    id_cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, related_name='ventas', db_column='id_cliente', default=0)
    id_producto_1 = models.ForeignKey(Inventario, on_delete=models.CASCADE, related_name='ventas_producto_1', null=True, blank=True, db_column='id_producto_1')
    cantidad_producto_1 = models.IntegerField(null=True, blank=True)
    id_producto_2 = models.ForeignKey(Inventario, on_delete=models.CASCADE, related_name='ventas_producto_2', null=True, blank=True, db_column='id_producto_2')
    cantidad_producto_2 = models.IntegerField(null=True, blank=True)
    id_producto_3 = models.ForeignKey(Inventario, on_delete=models.CASCADE, related_name='ventas_producto_3', null=True, blank=True, db_column='id_producto_3')
    cantidad_producto_3 = models.IntegerField(null=True, blank=True)
    id_producto_4 = models.ForeignKey(Inventario, on_delete=models.CASCADE, related_name='ventas_producto_4', null=True, blank=True, db_column='id_producto_4')
    cantidad_producto_4 = models.IntegerField(null=True, blank=True)
    id_producto_5 = models.ForeignKey(Inventario, on_delete=models.CASCADE, related_name='ventas_producto_5', null=True, blank=True, db_column='id_producto_5')
    cantidad_producto_5 = models.IntegerField(null=True, blank=True)
    fecha = models.DateField()
    
    def __str__(self):
        return f'Venta del {self.fecha} para {self.cliente}'
    
    class Meta:
        db_table = 'ventas'

class RegistroVentas(models.Model):
    id_productos_vendidos = models.ForeignKey(Ventas, on_delete=models.CASCADE, related_name='registro_ventas', db_column='id_productos_vendidos', default=0)
    id_forma_pago = models.ForeignKey(Catalogos, on_delete=models.CASCADE, related_name='formas_pago', db_column='id_forma_pago')
    id_estado_venta = models.ForeignKey(Catalogos, on_delete=models.CASCADE, related_name='estados_ventas', db_column='id_estado_venta')
    
    def __str__(self):
        return f'Registro de venta {self.venta.id}'
    
    class Meta:
        db_table = 'registro_ventas'

        
