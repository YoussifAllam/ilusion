
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status  
from apps.products.models import Products, Category,Home_OurProducts
from rest_framework.pagination import PageNumberPagination
from .background_Tasks import check_sale_prices
from .services import *




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
    
    #background task to check is the sale price time is end then return it to 0
    check_sale_prices.delay()

    products = Home_OurProducts.objects.all()
    serializer = Home_Products_Serializer(products, many=True)
    special_products = Products.objects.filter(IS_spacial_product=True)
    serializer2 = Category_Products_Serializer(special_products, many=True)
    Popup_data = get_signup_descount()
    Popup_data = {
        'content' : Popup_data[0][0],
        'discount' : Popup_data[0][1],
        'is_active' : Popup_data[0][2]
    }
    return Response(
        {
        'status':'success',

        'data' : {
            'Popup' : Popup_data  ,
        'OUR PRODUCTS': serializer.data , 
        'SPECIAL PRODUCTS' : serializer2.data
        }
        
        } , status=status.HTTP_200_OK)


