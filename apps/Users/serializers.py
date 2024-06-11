from .models import User 
from rest_framework import serializers
import re
from django.contrib.auth.password_validation import validate_password
import random



class SingUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'email', 'password',]
        extra_kwargs = {'password': {'write_only': True},
                        'email': {'required': True},
                        'username': {'read_only': True},
                        }

    def validate_email(self, value):
        # Check if email is already registered
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")

        return value

    def validate_password(self, value):
        # Check for strong password
        if not re.search(r'\d', value) or not re.search('[A-Z]', value):
            raise serializers.ValidationError("Password should contain at least 1 number and 1 uppercase letter.")

        validate_password(value)
        return value

    def create(self, validated_data):
        name = validated_data['name']
        email = validated_data['email']
        password = validated_data['password']

        # Generate a unique username if the provided name already exists as a username
        base_username = re.sub(r'\s+', '_', name).lower()
        unique_username = base_username
        while User.objects.filter(username=unique_username).exists():
            random_number = random.randint(1000, 9999)
            unique_username = f"{base_username}_{random_number}"

        user = User.objects.create_user(
            username=unique_username,
            email=email,
            password=password
        )
        user.name = name# Set is_startup based on validated data
        user.save()

        return user
    
class UserSerializer(serializers.ModelSerializer):
    # profile_picture = serializers.ImageField(required=False)
    class Meta:
        model = User
        fields = ('username','name' ,'email') 
        
        
