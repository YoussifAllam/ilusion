from django.urls import path
from .views import *

urlpatterns = [
    path('Order/', Order.as_view(), name='order_create'),
    path('OrderItems/' , OrderItems.as_view(), name='order_items') ,
    path('get_user_orders/' , get_user_orders)
]