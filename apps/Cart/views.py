from .models import *
from .serializers import CartSerializer , GetItemSerializer
from apps.products.models import ProductSize
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status  
from .services import Check_if_Cart_Item_Exists , calculate_total_price , calc_total_price_with_coupon
from apps.Coupons.models import Coupon


@api_view(['POST'])
def create_cart(request):
    if request.method == 'POST':
        cart = Cart.objects.create()
        return Response(
            {'status': 'success', 
            'cart_id': cart.id} ,  status=status.HTTP_201_CREATED)
    
@api_view(['POST'])
def add_item(request):
    if request.method == 'POST':
        target_product_size_uuid = request.data.get('product_size_uuid')
        Cart_id = request.data.get('cart_id')
        quantity = request.data.get('quantity', 1)
        try :  product_size = ProductSize.objects.get(product_size_uuid=target_product_size_uuid)
        except ProductSize.DoesNotExist: return Response({'status': 'fialed' , 'error': 'Product size not found'}, status=status.HTTP_404_NOT_FOUND)

        try :  cart = Cart.objects.get(id=Cart_id)
        except Cart.DoesNotExist: return Response({'status': 'fialed' , 'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

        is_cart_item_founded , cart_items = Check_if_Cart_Item_Exists(cart_id=Cart_id, product_size_id=product_size.id)
        if is_cart_item_founded:
            cart_items.quantity += int(quantity)
            cart_items.save()
        else : 
            cart_items = Cart_Items.objects.create(cart=cart, product_size=product_size, quantity=quantity)

        return Response(
            {'status': 'success', 
            'cart_items': cart_items.id} ,  status=status.HTTP_201_CREATED)
    
@api_view(['GET'])
def get_cart_details(request):
    if request.method == 'GET':
        cart_id = request.GET.get('cart_id')
        if not cart_id:
            return Response({'status': 'fialed' , 'error': 'Cart ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cart = Cart.objects.get(id=cart_id)
            serializer = CartSerializer(cart)
            return Response({
                'status': 'success',
                'data': serializer.data
            })
        except Cart.DoesNotExist:
            return Response({'status': 'fialed' , 'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def remove_item_from_cart(request): 
    if request.method == 'DELETE':
        cart_item_id = request.GET.get('cart_item_id')
        if not cart_item_id:
            return Response({'status': 'fialed' , 'error': 'cart_item_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cart_item = Cart_Items.objects.get(id=cart_item_id)
            cart_item.delete()
            return Response({'status': 'success' , 'message' :   'cart item deleted successfully'} , status=status.HTTP_200_OK)
        except Cart_Items.DoesNotExist:
            return Response({'status': 'fialed' , 'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def reduce_quantity(request):
    if request.method == 'POST':
        cart_item_id = request.data.get('cart_item_id')
        if not cart_item_id:
            return Response({'status': 'fialed' , 'error': 'cart_item_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cart_item = Cart_Items.objects.get(id=cart_item_id)
            if cart_item.quantity != 0:
                cart_item.quantity -= 1
                cart_item.save()
            else : 
                cart_item.delete()

            return Response({'status': 'success' , 'message' :  'quantity reduced successfully'} , status=status.HTTP_200_OK)
        except Cart_Items.DoesNotExist:
            return Response({'status': 'fialed' ,  'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['PATCH'])
def edit_quantity(request):
    if request.method == 'PATCH':
        cart_item_id = request.GET.get('cart_item_id')
        quantity = request.GET.get('quantity')

        if not cart_item_id or not quantity:
            return Response({'status': 'failed', 'error': 'cart_item_id and quantity are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            cart_item = Cart_Items.objects.get(id=cart_item_id)
            if int(quantity) <= 0:
                return Response({'status': 'failed', 'error': 'Quantity cannot be less than or equal to zero'}, status=status.HTTP_400_BAD_REQUEST)
            
            cart_item.quantity = quantity
            cart_item.save()

            serializer = GetItemSerializer(cart_item)
            return Response({'status': 'success', 'message': 'quantity edited successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        
        except Cart_Items.DoesNotExist:
            return Response({'status': 'failed', 'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['DELETE'])
def clear_shopping_cart(request): 
    if request.method == 'DELETE':
        cart_id = request.GET.get('cart_id')
        if not cart_id:
            return Response({'status': 'fialed' , 'error': 'cart_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cart = Cart.objects.get(id=cart_id)
            cart.delete()
            return Response({'status': 'success' , 'message' :  'cart  deleted successfully'}
                            , status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({'status': 'fialed' , 'error': 'cart not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def cart_total_price(request):
    cart_id = request.GET.get('cart_id')
    coupon_code = request.GET.get('coupon_code')
    try:
        cart = Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:
        return Response({'status': 'fialed' , 'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
    
    cart_items = cart.items.all()
    Subtotal , total_price_without_coupon , Shipping_Flat_rate = calculate_total_price(cart_items )
    
    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code)
        except Coupon.DoesNotExist:
            return Response({'status': 'fialed' , 'error': 'Coupon not found'}, status=status.HTTP_404_NOT_FOUND)
        
        sale_price , total_price ,  is_coupon_valid = calc_total_price_with_coupon(Subtotal , coupon)
        if not is_coupon_valid : 
            return Response({ 'status': 'field', 'coupon' : 'the_coupon_is_expired' , }, status=status.HTTP_400_BAD_REQUEST)
        else : 
            return Response({ 'status': 'success','total_price_without_coupon': Subtotal , 'total_price_after_coupon' : sale_price ,
                               'Shipping_Flat_rate' : Shipping_Flat_rate ,'total_price': total_price}, status=status.HTTP_200_OK)

    return Response({ 'status': 'success', 'subtotal' : Subtotal  , 'Shipping_Flat_rate' : Shipping_Flat_rate,
                     'total_price': total_price_without_coupon}, status=status.HTTP_200_OK)
