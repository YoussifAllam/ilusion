from .serializers import *
from rest_framework.response import Response
from apps.products.models import Products, Category
from django.db.models import Min, Max
from apps.Popup.models import Popup
from collections import defaultdict
from .services import *



def get_rating_details():
    ratings = Product_Rating.objects.values('Targer_Product', 'Rating_stars')
    product_star_count = defaultdict(set)
    
    for rating in ratings:
        star = rating['Rating_stars']
        product_id = rating['Targer_Product']
        # star_count[star] += 1
        product_star_count[star].add(product_id)
    
    ratings_detail = []
    for star in range(1, 6):  # Assuming rating stars are from 1 to 5
        num_of_products = len(product_star_count[star])
        if num_of_products != 0:
            ratings_detail.append({
                'stars': star,
                'product_count': num_of_products
            })
    
    result = {
        'ratings_detail': ratings_detail
    }
    
    
    return result



# @api_view(['GET'])
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


def get_signup_descount():
    signup_descount = Popup.objects.filter(id = 1).values_list('content', 'discount', 'is_active')

    return( signup_descount)


