from django.urls import path 
from .views import *
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('Get_Shop_products/', Get_Shop_products),
    path('Get_products_by_category/', products_by_category, name='products-by-category'),
    path('add_Product_rate/', add_Product_rate),
]
