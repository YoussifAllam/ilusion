from apps.products.models import Products, ProductSize, ProductImages, Product_Rating, Category, Home_OurProducts
from rest_framework import serializers


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ['size', 'Product_regular_price', 'Product_sale_price', 'is_available']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['ProductImage']

class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Rating
        fields = ['User_Name', 'Rating_stars', 'rate_content' , 'uploaded_at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['Category_id' ,'Category_name']

class RelatedProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True, source='Product_category')
    average_rating = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True, source='productimages_set')
    class Meta:
        model = Products
        fields = ['Product_id', 'Product_name', 'category' , 'average_rating', 'price_range', 'images']

    def get_average_rating(self, obj):
        ratings = obj.product_rating_set.all()
        if ratings.exists():
            return sum(rating.Rating_stars for rating in ratings) // ratings.count()
        return 0

class Category_Products_Serializer(serializers.ModelSerializer):
    sizes = ProductSizeSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True, source='productimages_set')
    average_rating = serializers.SerializerMethodField()
    number_of_ratings = serializers.SerializerMethodField()
    category = CategorySerializer(many=True, read_only=True, source='Product_category')
    reviews = ProductRatingSerializer(many=True, read_only=True ,source='product_rating_set')
    related_products = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = ['Product_id', 'Product_name','price_range' , 'sizes',  'SKU', 'category',
                    'images', 'average_rating', 'number_of_ratings'  ,'Product_description', 'reviews', 'IS_spacial_product'
                    , 'related_products'
                  ]

    def get_average_rating(self, obj):
        ratings = obj.product_rating_set.all()
        if ratings.exists():
            return sum(rating.Rating_stars for rating in ratings) // ratings.count()
        return 0

    def get_number_of_ratings(self, obj):
        return obj.product_rating_set.count()
    
    def get_related_products(self, obj):
        related_products = Products.objects.filter(Product_category__in=obj.Product_category.all()).exclude(Product_id=obj.Product_id)[:4]
        return RelatedProductSerializer(related_products, many=True).data

class AverageRatingSerializer(serializers.Serializer):
    average_rating = serializers.FloatField()
    rating_count = serializers.IntegerField()

class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Rating
        fields = ['Targer_Product', 'User_Name', 'Rating_stars', 'rate_content']
