from django.urls import path 

from . import views

app_name = "videojuegos"
urlpatterns = [
    path("", views.index, name="index"),
    path("clientes/", views.clientes, name="clientes"),
    path('clientes/registro/', views.ingresar_cliente, name='registro'),
    path('clientes/actualizar/', views.actualizar_cliente, name='actualizacion'),
    path('clientes/actualizar/<str:cedula>/', views.actualizar_cliente, name='actualizar_cliente'),
]
