from rest_framework.serializers import Serializer, CharField, UUIDField
from rest_framework.exceptions import ValidationError
# from ..Tasks import serializers_tasks
from ..models import *


class UpdateUserPasswordSerializer(Serializer):
    old_password = CharField(required=True)
    new_password = CharField(required=True)
    confirm_password = CharField(required=True)

    # def validate_old_password(self, value):
    #     user = self.context['request'].user
    #     if not check_password(value, user.password):
    #         raise ValidationError("Old password is incorrect.")
    #     return value

    # # Validate new password strength
    # def validate_new_password(self, value):
    #     if not serializers_tasks.validate_password_strength(value):
    #         raise ValidationError("New password is too weak.")
    #     return value

    # # Cross-field validation to check if new_password matches confirm_password
    # def validate(self, data):
    #     new_password = data.get('new_password')
    #     confirm_password = data.get('confirm_password')

    #     if new_password != confirm_password:
    #         raise ValidationError(
    #             {"confirm_password": "New password and confirm password do not match."}
    #         )
    #     return data
