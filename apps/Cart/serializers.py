from rest_framework import serializers
from .models import Cart , Cart_Items
from apps.products.models import ProductSize ,ProductImages , Products


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['ProductImage']

class ProductSizeSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = ProductSize
        fields = ['product_size_uuid' , 'product_name' , 'product', 'size', 'Product_regular_price', 'Product_sale_price', 'product_image']

    def get_product_image(self, obj):
        product_image = obj.product.productimages_set.first()
        if product_image:
            return ProductImagesSerializer(product_image).data['ProductImage']
        return None
    
    def get_product_name(self, obj):
        return obj.product.Product_name

class CartItemSerializer(serializers.ModelSerializer):
    product_size = ProductSizeSerializer()
    SUBTOTAL = serializers.SerializerMethodField()

    class Meta:
        model = Cart_Items
        fields = ['id', 'cart', 'quantity', 'SUBTOTAL', 'product_size']

    def get_SUBTOTAL(self, obj):
        if obj.product_size.Product_sale_price > 0:
            return obj.product_size.Product_sale_price * obj.quantity
        return obj.product_size.Product_regular_price * obj.quantity

class GetItemSerializer(serializers.ModelSerializer): # use it to get item data after editing it 
    product_size = ProductSizeSerializer()
    SUBTOTAL = serializers.SerializerMethodField()

    class Meta:
        model = Cart_Items
        fields = ['id', 'cart', 'quantity', 'SUBTOTAL', 'product_size']

    def get_SUBTOTAL(self, obj):
        sale_price = float(obj.product_size.Product_sale_price)
        regular_price = float(obj.product_size.Product_regular_price)
        quantity = int(obj.quantity)
        
        if sale_price > 0:
            return sale_price * quantity
        return regular_price * quantity


# class Item_serializer(serializers.ModelSerializer):
#     product_size = ProductSizeSerializer()

#     class Meta:
#         model = Cart_Items
#         fields = ['id', 'quantity', 'product_size']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'items']
