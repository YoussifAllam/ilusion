from celery import shared_task
from apps.products.models import ProductSize
from datetime import datetime
# Create your views here.




@shared_task
def check_sale_prices():
    all_products = ProductSize.objects.all()
    today_date = datetime.today().date()
    for product in all_products:
        try :
            if product.Sale_price_time_end.date() <= today_date : 
                product.Product_sale_price = 0
                product.Sale_price_time_end = None
                product.save()
        except Exception:
            pass


        