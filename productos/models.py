from django.db import models

# Create your models here.
class Product(models.Model):
    id_product = models.AutoField(primary_key=True, auto_created=True)
    name_product = models.CharField(max_length=50)
    price_product = models.FloatField()
    image_product = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id_product} - {self.name_product}"