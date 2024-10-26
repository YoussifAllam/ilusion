from rest_framework.serializers import ModelSerializer, CharField, BooleanField, ImageField, ValidationError , EmailField
from ..models import *


class QRCodeSerializer(ModelSerializer):
    class Meta:
        model = User_Qr_Code_image
        fields = ['memberShip_number']


class UserSerializer(ModelSerializer):
    memberShip_name = CharField(source='memberShip_fk.name', read_only=True)
    memberShip_number = QRCodeSerializer(source = 'User_Qr_Code_Set')

    class Meta:
        model = User_model
        fields = ['name', 'phone', 'profile_image', 'memberShip_name', 'memberShip_number']
