from rest_framework.serializers import ModelSerializer, CharField, BooleanField, ImageField, ValidationError , EmailField
from ..models import *
# from ..Tasks import serializers_tasks
# from ..db_queries import  services


class BillsSerializer(ModelSerializer):
    class Meta:
        model = Bills_model
        fields = ['serial_number', 'user_fk', 'amount', 'date' , 'bill_image']
        extra_kwargs = {
            'serial_number': {'required': False, } , 
            'amount': {'required': False, },
            'bill_image': {'required': False, }
        }