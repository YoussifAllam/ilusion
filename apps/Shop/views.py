from .serializers import *
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework import status  
from apps.products.models import Products, Category
from rest_framework.pagination import PageNumberPagination
from django.db.models import Avg, Count, Min, Max
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
User = get_user_model()

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
def Get_Shop_products(request):
    
    Target_products = Products.objects.all()
    
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_Product_rate(request):
    try:
        target_product = Products.objects.get(Product_id=request.data.get('Targer_Product_id'))
    except Products.DoesNotExist:
        return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

    target_user = request.user

    target_data = {
        'Rating_stars': request.data.get('Rating_stars'),
        'Targer_Product': target_product.Product_id,
        'User_Name': target_user.name,
        'rate_content': request.data.get('rate_content'),
    }

    serializer = ProductRatingSerializer(data=target_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


