from django.urls import path 

from . import views

app_name = "videojuegos"
urlpatterns = [
    path("", views.index, name="index"),
    path("clientes/", views.clientes, name="clientes"),
    path('clientes/ingresar/', views.ingresar_cliente, name='ingresar_cliente'),
    path('clientes/actualizar/<str:cedula>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('clientes/consultar/', views.consultar_cliente, name='consultar_cliente'),
    path("inventario/", views.inventario, name="inventario"),
    path('inventario/ingresar/', views.ingresar_inventario, name='ingresar_inventario'),
    path('inventario/actualizar/<str:codigo_producto>/', views.actualizar_inventario, name='actualizar_inventario'),
    path('inventario/consultar/', views.consultar_inventario, name='consultar_inventario'),
    path("catalogos/", views.catalogos, name="catalogos"),
    path('catalogos/ingresar/', views.ingresar_catalogo, name='ingresar_catalogo'),
    path('catalogos/actualizar/<int:id>/', views.actualizar_catalogo, name='actualizar_catalogo'),
    path('ventas/', views.ventas, name='ventas'),
    path('ventas/ingresar/', views.ingresar_venta, name='ingresar_venta'),
    path('ventas/consultar/', views.consultar_venta, name='consultar_venta'),
    path('ventas/detalles/<int:id>/', views.detalles_venta, name='detalles_venta'),
]
