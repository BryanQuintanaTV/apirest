from django.db import models
from productos.models import Product

# Class (Table's name)
class Order(models.Model):
    # Names and types of each column of the table
    num_order = models.AutoField(primary_key=True)
    total_order = models.DecimalField(max_digits=10, decimal_places=2)
    date_order = models.DateField()
    id_user = models.IntegerField()

    products = models.ManyToManyField(
        'productos.Product',
        through='OrderProduct',
        related_name='orders',
    )


class OrderProduct(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey('productos.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

