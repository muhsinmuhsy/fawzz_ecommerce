from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_image', null=True, blank=True)
    image_two = models.ImageField(upload_to='product_image', null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    actual_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.BooleanField(default=True)
    def __str__(self):
        return self.name
 