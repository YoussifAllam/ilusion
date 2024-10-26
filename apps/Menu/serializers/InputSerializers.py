from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    BooleanField,
    ImageField,
    ValidationError,
    EmailField,
)
from ..models import *
from ..db_queries import services


class SignUpSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
        ]
        extra_kwargs = {
        }

    # def validate_email(self, value: str):
    #     pass

    # def validate_password(self, value: str):
    #     pass

    # def validate(self, data: dict):
    #     pass

    # def create(self, validated_data: dict):
    #     pass
