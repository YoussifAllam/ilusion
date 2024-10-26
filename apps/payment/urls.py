from django.urls import path
from .views import PaymentView

urlpatterns = [
    path('payment/pay/', PaymentView.as_view(), name='payment'),
]