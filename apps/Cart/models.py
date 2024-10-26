from django.db import models
from uuid import uuid4
# Create your models here.

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Cart_Items(models.Model):
    id  = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    product_size = models.ForeignKey('products.ProductSize', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'Cart'
        ordering = ['-date_added']

    def __str__(self):
        return f"{self.quantity} x {self.product_size.product.Product_name} - {self.product_size.size}"