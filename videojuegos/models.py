from django.db import models

# Create your models here.
class Clientes (models.Model):
    cedula = models.CharField(max_length=10, null=False, unique=True)
    apellidos_nombres = models.CharField(max_length=100, null=False)
    correo = models.CharField(max_length=100, null=False, unique=True)
    provincia = models.CharField(max_length=50, null=False)
    direccion = models.CharField(max_length=100, null=False)
    id_estado_cliente = models.IntegerField(null=False)
    telefono = models.CharField(max_length=10, null=False, unique=True)
    
    def __str__(self) -> str:
        return f'{self.apellidos_nombres}'
    
    class Meta:
        db_table = 'clientes'