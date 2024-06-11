from django.urls import path 
from .views import *
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('Get_Home_OurProducts/', Get_home_OurProducts),
    path('Get_products_by_category/', products_by_category, name='products-by-category'),
    
]
