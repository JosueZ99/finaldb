# Generated by Django 4.2 on 2024-08-03 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videojuegos', '0005_alter_inventario_id_estado_producto_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventario',
            name='codigo_producto',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
