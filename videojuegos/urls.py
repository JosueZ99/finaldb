from django.urls import path 

from . import views

app_name = "videojuegos"
urlpatterns = [
    path("", views.index, name="index"),
    path("clientes/", views.clientes, name="clientes"),
    path('clientes/registro/', views.ingresar_cliente, name='registro'),
    path('clientes/actualizar/<str:cedula>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('clientes/consultar/', views.consultar_cliente, name='consultar_cliente'),
    path("inventario/", views.inventario, name="inventario"),
    path('inventario/ingresar/', views.ingresar_inventario, name='ingresar'),
    path('inventario/actualizar/<str:codigo_producto>/', views.actualizar_inventario, name='actualizar_inventario'),
    path('inventario/consultar/', views.consultar_inventario, name='consultar_inventario'),
]
