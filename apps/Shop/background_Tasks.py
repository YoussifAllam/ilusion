from celery import shared_task
from apps.products.models import ProductSize
from datetime import datetime
# Create your views here.
from django.core.mail import send_mail
from django.conf import settings



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

    # send_mail('full_subject', 'full_message', settings.DEFAULT_FROM_EMAIL, ['youssifhassan011@gmail.com'])




        