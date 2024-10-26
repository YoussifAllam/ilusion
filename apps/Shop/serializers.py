from apps.products.models import Products, ProductSize, ProductImages, Product_Rating, Category
from rest_framework import serializers


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = [ 'product_size_uuid', 'size', 'Product_regular_price', 'Product_sale_price', 'is_available']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['ProductImage']

class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Rating
        fields = ['Rating_stars', 'Targer_Product', 'User_Name', 'rate_content' ,'uploaded_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['Targer_Product'] = instance.Targer_Product.Product_name  # Display product name
        return representation

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['Category_id' ,'Category_name']

class RelatedProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True, source='Product_category')
    average_rating = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True, source='productimages_set')    
    number_of_ratings = serializers.SerializerMethodField()
    class Meta:
        model = Products
        fields = ['Product_id', 'Product_name', 'category' , 'average_rating', 'number_of_ratings' , 'price_range', 'images']

    def get_average_rating(self, obj):
        ratings = obj.product_rating_set.all()
        if ratings.exists():
            return sum(rating.Rating_stars for rating in ratings) // ratings.count()
        return 0
    
    def get_number_of_ratings(self, obj):
        return obj.product_rating_set.count()

class Category_Products_Serializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    number_of_ratings = serializers.SerializerMethodField()
    category = CategorySerializer(many=True, read_only=True, source='Product_category')

    class Meta:
        model = Products
        fields = ['Product_id', 'Product_name','price_range' ,  'category',
                    'images', 'average_rating', 'number_of_ratings'  ,'Product_description'
                    
                  ]

    def get_average_rating(self, obj):
        ratings = obj.product_rating_set.all()
        if ratings.exists():
            return sum(rating.Rating_stars for rating in ratings) // ratings.count()
        return 0

    def get_number_of_ratings(self, obj):
        return obj.product_rating_set.count()
    
    def get_images(self, obj):
        return [f"media/{image.ProductImage.name}" for image in obj.productimages_set.all()]

class GEt_Products_by_id_Serializer(serializers.ModelSerializer):
    sizes = ProductSizeSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True, source='productimages_set')
    average_rating = serializers.SerializerMethodField()
    number_of_ratings = serializers.SerializerMethodField()
    category = CategorySerializer(many=True, read_only=True, source='Product_category')
    related_products = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = ['Product_id', 'Product_name','price_range' , 'sizes',  'SKU', 'category',
                    'images', 'average_rating', 'number_of_ratings'  ,'Product_description'
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

class RatingDetailSerializer(serializers.Serializer):
    stars = serializers.IntegerField()
    # count = serializers.IntegerField()
    product_count = serializers.IntegerField()

class AverageRatingSerializer(serializers.Serializer):
    # rating_count = serializers.IntegerField()
    ratings_detail = RatingDetailSerializer(many=True)
    
class Products_search_Serializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = ['Product_id', 'Product_name','price_range' , 'images' ]

    def get_images(self, obj):
        return [f"media/{image.ProductImage.name}" for image in obj.productimages_set.all()]
    

