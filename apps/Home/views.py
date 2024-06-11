
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status  
from apps.products.models import Products, Category,Home_OurProducts
from rest_framework.pagination import PageNumberPagination
from django.db.models import Avg, Count, Min, Max


# @api_view(['GET'])
def get_shop_data(request):
    # Get categories
    categories = Category.objects.all()
    categories_serializer = CategorySerializer(categories, many=True)

    # Get average rating and rating count
    rating_data = Product_Rating.objects.aggregate(
        average_rating=Avg('Rating_stars'),
        rating_count=Count('Rating_stars')
    )
    average_rating_serializer = AverageRatingSerializer(rating_data)

    # Get price range
    price_data = Products.objects.aggregate(
        min_price=Min('sizes__Product_regular_price'),
        max_price=Max('sizes__Product_regular_price')
    )

    # Construct response data
    response_data = {
        'categories': categories_serializer.data,
        'average_rating': (average_rating_serializer.data['average_rating'] // 1),
        'rating_count': average_rating_serializer.data['rating_count'],
        'min_price': price_data['min_price'],
        'max_price': price_data['max_price']
    }

    return Response(response_data)


@api_view(['GET'])
def products_by_category(request):
    category_uuid = request.data.get('category_uuid')
    if not category_uuid:
        return Response({"detail": "category_uuid is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        category = Category.objects.get(Category_id=category_uuid)
        Target_products = Products.objects.filter(Product_category=category)
    except Category.DoesNotExist:
        return Response({"detail": "Category not found or no products in this category."}, status=status.HTTP_404_NOT_FOUND)
    
    # Apply pagination
    paginator = PageNumberPagination()
    paginator.page_size = 12  # or use CustomPagination class
    paginated_products = paginator.paginate_queryset(Target_products, request)
    
    serializer = Category_Products_Serializer(paginated_products, many=True)
    paginated_response = paginator.get_paginated_response(serializer.data)
    
    # Add custom status field to the response data
    paginated_response.data['status'] = 'success'

    slide_bar_data = get_shop_data(request)
    
    # return paginated_response
    response_data = {
        'status': 'success',
        'Slide Bar' : slide_bar_data.data ,
        'Products': {
        'count': paginated_response.data['count'],
        'next': paginated_response.data['next'],
        'previous': paginated_response.data['previous'],
        'results': paginated_response.data['results']
        }

    }
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def Get_home_OurProducts(request):
    products = Home_OurProducts.objects.all()
    serializer = Home_Products_Serializer(products, many=True)
    special_products = Products.objects.filter(IS_spacial_product=True)
    serializer2 = Category_Products_Serializer(special_products, many=True)
    return Response(
        {
        'status':'success',
        'data' : {
        'OUR PRODUCTS': serializer.data , 
        'SPECIAL PRODUCTS' : serializer2.data
        }
        
        } , status=status.HTTP_200_OK)


