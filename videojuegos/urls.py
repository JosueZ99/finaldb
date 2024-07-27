from django.urls import path 

from . import views

app_name = "videojuegos"
urlpatterns = [
    path("", views.index, name="index"),
    path('registro/', views.ingresar_o_actualizar_cliente, name='registro'),
]
