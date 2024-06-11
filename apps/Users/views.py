from .serializers import SingUpSerializer,UserSerializer 


from rest_framework import viewsets, status 
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.decorators import action
from django.contrib.auth import get_user_model

import random
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import  login as django_login
from django.contrib.auth import logout
from rest_framework.decorators import api_view, permission_classes,parser_classes
from django.contrib.auth.hashers import make_password

from django.utils.crypto import get_random_string
from datetime import datetime, timedelta
from .permissions import IsAdminOrPostOnly 
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.parsers import MultiPartParser, FormParser

import re   
from django.utils.timezone import now
User = get_user_model()

from django.conf import settings

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SingUpSerializer
    permission_classes = [IsAdminOrPostOnly]

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            refresh = RefreshToken.for_user(user)
            token_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            return Response({'user': serializer.data, 'tokens': token_data}, status=status.HTTP_201_CREATED)
        else:
            email_errors = serializer.errors.get('email', [])
            password_errors = serializer.errors.get('password', [])

            if email_errors:
                return Response({'message': email_errors[0]}, status=status.HTTP_400_BAD_REQUEST)
            elif password_errors:
                return Response({'message': password_errors[0]}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = UserSerializer(request.user, many=False)
    return Response(user.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_user(request):
    user = request.user
    data = request.data

    user.name = data.get('name', user.name)
    if 'profile_picture' in request.data:
        user.profile_picture = request.data['profile_picture']
        if user.profile_picture:
            user.profile_picture = request.data['profile_picture']
        else:
            # Set default profile picture if 'profile_picture' is not provided or empty
            user.profile_picture = 'default.jpg'


    if 'old_password' in data or 'password' in data:
        PASSWORD_PATTERN = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

        if 'old_password' in data and 'new_password' in data and 'confirm_password' in data:
            old_password = data['old_password']
            new_password = data['new_password']
            confirm_password = data['confirm_password']

            # Check if the new password and confirm password are not empty
            if new_password and confirm_password:
                # Verify that the old password matches the user's current password
                if user.check_password(old_password):
                    # Check if the new password is the same as the old password
                    if new_password != old_password:
                        # Check if the new password and confirm password match
                        if new_password == confirm_password:
                            # Check if the new password meets the strength requirements
                            if re.match(PASSWORD_PATTERN, new_password):
                                # Set the new password
                                user.set_password(new_password)
                                # Save the user object
                                user.save()
                            else:
                                # Return an error response indicating that the password does not meet the strength requirements
                                return Response({"message": "The password must contain upper and lower case letters, a number and at least one symbol"}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            # Return an error response indicating that the new password and confirm password do not match
                            return Response({"message": "Mismatched password"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        # Return an error response indicating that the new password is the same as the old password
                        return Response({"message": "The new password should be different"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # Return an error response indicating that the old password is incorrect
                    return Response({"message": "Incorrect old password"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Return an error response indicating that the new password or confirm password is empty
                return Response({"message": "Please fill in the new password and confirm the password"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Return an error response indicating that the required fields are missing
            return Response({"message": "Old password, new password, and confirm password are required"}, status=status.HTTP_400_BAD_REQUEST)

    if 'phone_number' in data:
        user.phone_number = data['phone_number']

    user.save()
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

def get_current_host(request):
    protocol = request.is_secure() and 'https' or 'http'
    host = request.get_host()
    return "{protocol}://{host}/".format(protocol=protocol, host=host)

@api_view(['POST'])
def forgot_password(request):
    data = request.data
    email = data.get('email')
    
    # Check if the email is provided and is not empty
    if not email:
        return Response({'detail': 'Email address is required.'}, status=400)
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Consider security practices here; in some cases, you might not want to reveal that an email does or doesn't exist in the system
        return Response({'detail': 'User not found.'}, status=404)
    
    token = get_random_string(40)
    expire_date = now() + timedelta(hours=10)
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date
    user.profile.save()
    
    
    # Be cautious about the amount of detail you reveal in success messages
    return Response({'details': 'If the email exists in our system, a password reset link has been sent.', 'link': link, 'token': token})

@api_view(['POST'])
def reset_password(request,token):
    data = request.data
    try:
        # print('====================' , token)
        user = User.objects.get(profile__reset_password_token=token)
    except User.DoesNotExist:
        return Response(
            {'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST
        )
    if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response({'message': 'الرابط منتهي'},status=status.HTTP_400_BAD_REQUEST)
    try:
        if not data['password'] or not data['confirmPassword']:
            return Response({'message': 'يجب ان تقوم بأدخال كلمه المرور'},status=status.HTTP_400_BAD_REQUEST)
        
    except : return Response({'message': 'يجب ان تقوم بأدخال كلمات المرور'},status=status.HTTP_400_BAD_REQUEST)
    
    if data['password'] != data['confirmPassword']:
        return Response({'message': 'كلمة المرور غير متطابقة'},status=status.HTTP_400_BAD_REQUEST)
    
    user.password = make_password(data['password'])
    user.profile.reset_password_token = ""
    user.profile.reset_password_expire = None 
    user.profile.save() 
    user.save()
    return Response({'message': 'تم تغيير كلمة المرور بنجاح'})

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None and user.check_password(password):
            if not user.is_active or not user.email_verified:
                return Response({'message': 'Your account has been deactivated'}, status=status.HTTP_403_FORBIDDEN)
            
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            django_login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return Response({'user': UserSerializer(user).data, 'tokens': data}, status=status.HTTP_200_OK)
        #check if email not exist
        elif user is None:
            return Response({'message': 'Email not found'}, status=status.HTTP_401_UNAUTHORIZED)
            
        else:
            return Response({'message': 'Email or Password is uncorrect'}, status=status.HTTP_401_UNAUTHORIZED)

class APILogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "OK, goodbye, all refresh tokens blacklisted"})
        refresh_token = self.request.data.get('refresh_token')
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        logout(request)
        return Response({"status": "OK, goodbye"})
    
