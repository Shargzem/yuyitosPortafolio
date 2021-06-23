# Generated by Django 3.2.4 on 2021-06-23 22:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20210623_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.category', verbose_name='Categoría'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_cost',
            field=models.DecimalField(decimal_places=0, default=0.0, max_digits=9, verbose_name='Precio Costo'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_sale',
            field=models.DecimalField(decimal_places=0, default=0.0, max_digits=9, verbose_name='precio Venta'),
        ),
    ]
