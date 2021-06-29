from django.db import models
from datetime import datetime
# Create your models here.
from django.forms import model_to_dict

from core.choices import gender_choices

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        db_table = 'categoria'
        ordering = ['id']


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    cate = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    #image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True)
    price_cost = models.DecimalField(default=0, max_digits=9, decimal_places=0, verbose_name='Precio Costo')
    price_sale = models.DecimalField(default=0, max_digits=9, decimal_places=0, verbose_name='precio Venta')


    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['cate'] = self.cate.toJSON()
        return item

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        db_table = 'producto'
        ordering = ['id']


class Client(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    surnames = models.CharField(max_length=150, verbose_name='Apellidos')
    rut = models.CharField(max_length=10, unique=True, verbose_name='Rut')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    gender = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Genero')

    def __str__(self):
        return self.names

    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        db_table = 'cliente'
        ordering = ['id']


class Sale(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0, max_digits=9, decimal_places=0)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=0)
    total = models.DecimalField(default=0, max_digits=9, decimal_places=0)

    def __str__(self):
        return self.cli.names

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        db_table = 'venta'
        ordering = ['id']


class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0, max_digits=9, decimal_places=0)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0, max_digits=9, decimal_places=0)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['prod'] = self.prod.toJSON()
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        db_table = 'detalle_venta'
        ordering = ['id']


class Order(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    cant = models.IntegerField(default=0)
    total = models.DecimalField(default=0, max_digits=9, decimal_places=0)
    date = models.DateField(default=datetime.now)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural = 'Ordenes'
        db_table = 'pedido'
        ordering = ['id']

class Supplier(models.Model):
    rut = models.CharField(max_length=10, unique=True, verbose_name='Rut')
    rs = models.CharField(max_length=150, verbose_name='Razon Social')
    turn = models.CharField(max_length=150, verbose_name='Giro')
    phone = models.IntegerField( verbose_name='Telefono')
    date = models.DateField(default=datetime.now)

    def __str__(self):
        return self.rs

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        db_table = 'proveedor'
        ordering = ['id']

class Lote(models.Model):
    date_ini = models.DateField(default=datetime.now)
    date_venc = models.DateField(default=datetime.now)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Orden')
    supp = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='Proveedor')


    def __str__(self):
        return self.order.name

    def toJSON(self):
        item = model_to_dict(self)
        item['order'] = self.order.toJSON()
        item['supp'] = self.supp.toJSON()
        return item

    class Meta:
        verbose_name = 'Lote'
        verbose_name_plural = 'Lotes'
        db_table = 'lote'
        ordering = ['id']


