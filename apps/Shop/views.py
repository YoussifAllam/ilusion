from .serializers import *
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework import status  
from apps.products.models import Products, Category , Product_Rating
from rest_framework.pagination import PageNumberPagination
from django.db.models import Avg , Q
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models import Func
from .services import sort_products , get_shop_data , pagenator
from .background_Tasks import check_sale_prices

class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 1)'  # rounding to 1 decimal place

@api_view(['GET'])
def Get_Shop_products(request):
    
    #background task to check is the sale price time is end then return it to 0
    check_sale_prices.delay()

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
    category_uuid = request.GET.get('category_uuid')
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
    product_id = request.data.get('target_product_id')
    if not product_id:
        return Response({"detail": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        target_product = Products.objects.get(pk=product_id)
    except Products.DoesNotExist:
        return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

    target_user = request.user  # Assuming your User model has a 'name' field

    target_data = {
        'Rating_stars': request.data.get('Rating_stars'),
        'Targer_Product': target_product.Product_id,  # Assign the product instance
        'User_Name': target_user.username,  # Adjusted to standard User model field
        'rate_content': request.data.get('rate_content'),
    }

    serializer = ProductRatingSerializer(data=target_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def Filter_Products(request):
    Target_products = Products.objects.all()

    num_of_Stars = request.GET.get('num_of_Stars')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    Category = request.GET.get('Category')
    will_sort = request.GET.get('sort?')

    if not num_of_Stars and not price_from and not price_to and not Category and not will_sort:
        return Response({"detail": "No filter applied."}, status=status.HTTP_400_BAD_REQUEST)

    if num_of_Stars:
        # Split the num_of_Stars by comma and convert to floats
        num_of_Stars = [float(star) for star in num_of_Stars.split(',')]
        # Create a Q object to hold the OR conditions for each star range
        star_conditions = Q()
        for star in num_of_Stars:
            star_conditions |= Q(rounded_average__gte=star, rounded_average__lt=star + 1)

        Target_products = Target_products.annotate(
            average_rating=Avg('product_rating__Rating_stars')
        ).annotate(
            rounded_average=Round('average_rating')
        ).filter(star_conditions)

    if price_from and price_to:
        # Filter products where either the regular price or the sale price is within the specified range
        Target_products = Target_products.filter(
            Q(sizes__Product_regular_price__gte=price_from, sizes__Product_regular_price__lte=price_to) |
            Q(sizes__Product_sale_price__gte=price_from, sizes__Product_sale_price__lte=price_to)
        ).distinct()

    elif price_from :
        Target_products = Target_products.filter(
            Q(sizes__Product_regular_price__gte=price_from) |
            Q(sizes__Product_sale_price__gte=price_from)
        ).distinct()
        
    elif price_to and not price_from:
        Target_products = Target_products.filter(
            Q(sizes__Product_regular_price__lte=price_to ) 
            | ( Q(sizes__Product_sale_price__lte=price_to ) & ~Q( sizes__Product_sale_price=0)  )
        ).distinct()

    if Category:
        Target_products = Target_products.filter(
            Product_category__Category_id__icontains=Category
        ).distinct()

    if will_sort == 'True':
        Target_products = sort_products(Target_products , request  )

    response_data =  pagenator(Target_products , request , 'Category_Products_Serializer')    
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def Get_product_by_id(request):
    product_id = request.GET.get('product_id')
    if not product_id:
        return Response({"detail": "product_id is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = Products.objects.get(Product_id=product_id)
    except Products.DoesNotExist:
        return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = GEt_Products_by_id_Serializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def Get_product_Ratings_by_id(request):
    product_id = request.GET.get('product_id')
    if not product_id:
        return Response({"detail": "product_id is required."}, status=status.HTTP_400_BAD_REQUEST)

    ratings = Product_Rating.objects.filter(Targer_Product__Product_id=product_id)
    if not ratings.exists():
        return Response({"detail": "Ratings not found for the given product_id."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductRatingSerializer(ratings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def Search(request):
    product_name = request.GET.get('product_name')
    will_sort = request.GET.get('will_sort')
    if not product_name:
        return Response({"detail": "product_name is required."}, status=status.HTTP_400_BAD_REQUEST)

    Target_products = Products.objects.filter(Product_name__icontains=product_name)
    if not Target_products.exists():
        return Response({"detail": "No products found for the given product_name."}, status=status.HTTP_404_NOT_FOUND)

    if will_sort == 'True':
        Target_products = sort_products(Target_products , request )

    
    response_data =  pagenator(Target_products , request , 'Products_search_Serializer')   

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def Get_all_Categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response({
        'status' : 'succes',
        'date': serializer.data}, status=status.HTTP_200_OK)


