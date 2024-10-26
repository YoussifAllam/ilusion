from rest_framework.serializers import Serializer, UUIDField , IntegerField , ImageField , CharField
from ..models import *
from rest_framework.exceptions import ValidationError

# class Check_vaild_refund_params(Serializer):
#     order_id = CharField(required=True)

class UserParamsSerializer(Serializer):
    id = UUIDField(required=True)

class BillSerializer(Serializer):
    user_id = UUIDField(required=True)
    bill_image = ImageField(required=False)
    serial_number = CharField(required=False)
    amount = IntegerField(required=False)

    def validate(self, data):
        user_id = data.get('user_id')
        bill_image = data.get('bill_image')
        serial_number = data.get('serial_number')
        amount = data.get('amount')

        # Check if the necessary fields are provided
        if not ((bill_image and not serial_number) or (serial_number and amount)):
            raise ValidationError(
                "You must provide either 'bill_image' or both 'serial_number' and 'amount'."
            )
        return data
    