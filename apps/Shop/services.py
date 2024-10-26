from django.db.models import Min, Max , Avg 
from apps.products.models import Products, Category , Product_Rating
from .serializers import AverageRatingSerializer , CategorySerializer ,Category_Products_Serializer , Products_search_Serializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from collections import defaultdict

def sort_products(Target_products, request):
    sort_by = request.GET.get('sort_by')
    if sort_by == 'low_to_high':
        Target_products = Target_products.order_by('sizes__Product_regular_price')
    elif sort_by == 'high_to_low':
        Target_products = Target_products.order_by('-sizes__Product_regular_price')
    elif sort_by == 'latest':
        Target_products = Target_products.order_by('uploaded_at')
    elif sort_by == 'popularity':
        Target_products = Target_products.order_by('-Product_id')
    elif sort_by == 'average_rating':
        Target_products = Target_products.annotate(
            average_rating=Avg('product_rating__Rating_stars')
        ).order_by('-average_rating')
    return Target_products

def get_rating_details():
    # Aggregate to compute the average rating for each product
    product_averages = Product_Rating.objects.values('Targer_Product').annotate(avg_rating=Avg('Rating_stars'))

    # Dictionary to hold the count of products for each average rating
    average_rating_count = defaultdict(int)

    # Collect data about how many products have each average rating
    for entry in product_averages:
        avg_rating_rounded = int(entry['avg_rating'])  # Round to one decimal place for grouping
        average_rating_count[avg_rating_rounded] += 1

    # Prepare the final list of average ratings and how many products have that average
    ratings_detail = []
    for avg_rating, count in sorted(average_rating_count.items()):
        ratings_detail.append({
            'stars': avg_rating,
            'product_count': count
        })

    result = {
        'ratings_detail': ratings_detail
    }

    return result

def get_shop_data(request):
    # Get categories
    categories = Category.objects.all()
    categories_serializer = CategorySerializer(categories, many=True)

    # Get price range
    price_data = Products.objects.aggregate(
        min_price=Min('sizes__Product_regular_price'),
        max_price=Max('sizes__Product_regular_price')
    )

    rating_details = get_rating_details()
    rating_seralizer = AverageRatingSerializer(rating_details)
    # Construct response data
    response_data = {
        'categories': categories_serializer.data,
        'rating_details': rating_seralizer.data['ratings_detail'],
        # 'rating_count': average_rating_serializer.data['rating_count'],
        'min_price': price_data['min_price'],
        'max_price': price_data['max_price']
    }

    return Response(response_data)

def pagenator(Target_products , request , serializer):
    paginator = PageNumberPagination()
    paginator.page_size = 12  # or use CustomPagination class
    paginated_products = paginator.paginate_queryset(Target_products, request)

    if serializer == 'Category_Products_Serializer':
        serializer = Category_Products_Serializer(paginated_products, many=True, context={'request': request})
    elif serializer == 'Products_search_Serializer':
        serializer = Products_search_Serializer(paginated_products, many=True, context={'request': request})

    paginated_response = paginator.get_paginated_response(serializer.data)
    
    # Add custom status field to the response data
    paginated_response.data['status'] = 'success'

    # return paginated_response
    response_data = {
        'status': 'success',
        'Products': {
        'count': paginated_response.data['count'],
        'next': paginated_response.data['next'],
        'previous': paginated_response.data['previous'],
        'results': paginated_response.data['results']
        }

    }
    return response_data



