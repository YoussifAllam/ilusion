from django.db import models
from uuid import uuid4
from django.core.validators import MaxValueValidator , MinValueValidator
# Create your models here.


class Products(models.Model):
    Product_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    Product_name = models.CharField(max_length=50, verbose_name='Product name')
    Product_description = models.TextField(verbose_name='Product description')
    Product_category = models.ManyToManyField('Category', verbose_name='Product Category')
    SKU = models.CharField(max_length=50, default='N/A', null=True, blank=True)
    IS_spacial_product = models.BooleanField(default=False)

    def __str__(self):
        return self.Product_name

    def price_range(self):
        sizes = self.sizes.all()
        if not sizes:
            return 'N/A'
        min_price = min(size.Product_regular_price for size in sizes)
        max_price = max(size.Product_regular_price for size in sizes)
        return f"${min_price} - ${max_price}"

    class Meta:
        verbose_name = 'Products'
        verbose_name_plural = 'Products'

class ProductSize(models.Model):
    product = models.ForeignKey('Products', related_name='sizes', on_delete=models.CASCADE)
    size = models.CharField(max_length=50, verbose_name='Size') 
    Product_regular_price = models.FloatField(verbose_name='Regular price $')
    Product_sale_price = models.FloatField(verbose_name='Sale price $' , default= 0)
    Sale_price_time_end = models.DateTimeField(verbose_name='Sale price time end' , null= True , blank = True)
    is_available = models.BooleanField(default=True , verbose_name= 'Is available ?')

    def __str__(self):
        return f"{self.product.Product_name} - {self.size}"

class ProductImages(models.Model):
    ProductImage_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    ProductImage = models.ImageField(upload_to='products_images/' , verbose_name='Product image')

class Category(models.Model):
    Category_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    Category_name = models.CharField(max_length=200 , verbose_name= 'Category name')


    def __str__(self):
        return self.Category_name
    
class Home_OurProducts(models.Model):
    name = models.CharField(max_length=200 , verbose_name= 'Name')
    Category = models.ForeignKey('Category', verbose_name='Category', on_delete=models.CASCADE , unique=True)
    Category_image = models.ImageField(upload_to='category_images/' , verbose_name='Category image' , null=True, blank=True)


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Our Products'
        verbose_name_plural = 'Our Products'

class Product_Rating(models.Model):
    Targer_Product = models.ForeignKey(Products , on_delete=models.CASCADE )
    User_Name = models.CharField(max_length=100 , verbose_name= 'User Name')
    Rating_stars = models.IntegerField(validators = [MinValueValidator(1) , MaxValueValidator(5)] , verbose_name= 'Rating stars' ) # to control min and max values
    uploaded_at = models.DateTimeField(auto_now_add=True)
    rate_content = models.TextField( verbose_name= 'Rate content')

    def __str__(self) -> str:
        return f"{self.Targer_Product} -- {self.User_Name}" 

    class Meta:
        unique_together = (('User_Name', 'Targer_Product'))
        index_together  = (('User_Name', 'Targer_Product'))

        verbose_name_plural = "Ratings"
        verbose_name = 'Ratings'
