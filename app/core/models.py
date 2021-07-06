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
    stock = models.IntegerField(default=0, verbose_name='Stock')
    price_cost = models.IntegerField(default=0, verbose_name='Precio Costo')
    price_sale = models.IntegerField(default=0, verbose_name='precio Venta')


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

    def get_full_name(self):
        return '{} {} / {}'.format(self.names, self.surnames, self.rut)

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
    subtotal = models.IntegerField(default=0)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.IntegerField(default=0)

    def __str__(self):
        return self.cli.names

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['iva'] = format(self.iva, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detsale_set.all()]
        return item

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        db_table = 'venta'
        ordering = ['id']


class DetSale(models.Model):
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    price = models.IntegerField(default=0, )
    cant = models.IntegerField(default=0)
    subtotal = models.IntegerField(default=0 )

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

class Credited(models.Model):
    date_joined = models.DateField(default=datetime.now)
    date_end = models.DateField(default=datetime.now, verbose_name='Fecha Termino')
    total = models.IntegerField(default=0, verbose_name='Total')
    payment = models.IntegerField(default=0, verbose_name='Abono')
    state = models.BooleanField(default=True)
    cli = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Cliente')

    def __str__(self):
        return self.cli.names

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['date_end'] = self.date_end.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Fiado'
        verbose_name_plural = 'Fiados'
        db_table = 'fiado'
        ordering = ['id']






class Order(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    cant = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
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
    email = models.CharField(max_length=150, verbose_name='Correo')
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
    prod = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto')


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


