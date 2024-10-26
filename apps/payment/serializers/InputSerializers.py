from rest_framework.serializers import Serializer , CharField , DecimalField 
# from apps.payment.models import *

class PaymentSerializer(Serializer):
    credit_card_number = CharField(max_length=16)
    expiration_date = CharField(max_length=5)  # Format: MM/YY
    card_code = CharField(max_length=4)
    amount = DecimalField(max_digits=10, decimal_places=2)
    # order_id = CharField(max_length=100)