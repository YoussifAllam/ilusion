from django.http import HttpRequest
from random import randint
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
    HTTP_401_UNAUTHORIZED,
)
from django.contrib.auth import login as django_login
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)
from django.contrib.auth import logout
from rest_framework.request import Request
from typing import Any
from datetime import timedelta, datetime
from . import celery_tasks
from ..serializers import OutputSerializers, ParamsSerializers
from .. import constant
from ..models import User
current_site = constant.CURRENT_SITE


def send_otp_to_user_email(user: User) -> dict:
    # Generate a 4-digit OTP and store it in the user's profile
    otp = randint(1000, 9999)
    user.otp = otp
    user.otp_created_at = timezone.now()

    user.save()

    # Send the OTP to the user via email

    subject = "Your verification OTP on {0}".format(current_site)
    html_message = constant.create_otp_template(
                f"{user.first_name} {user.last_name}", otp, user.email
            )
    # user.email_user(subject, message)
    celery_tasks.send_email_task.delay(user.id,  subject, html_message)

    refresh = RefreshToken.for_user(user)
    token_data = {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
    return token_data


def is_otp_valid(otp_created_at: datetime) -> bool:
    if otp_created_at:
        expiration_time = otp_created_at + timedelta(minutes=15)
        return timezone.now() <= expiration_time
    else:
        return False


def conferm_email_using_otp(request: HttpRequest) -> tuple[dict, int]:
    user_uuid = request.data.get("user_uuid")
    otp = request.data.get("otp")

    if not user_uuid or not otp:
        return ({"detail": "Missing user UUID or OTP."}, HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(uuid=user_uuid)
        if user.email_verified:
            return ({"detail": "Email already confirmed."}, HTTP_400_BAD_REQUEST)

        if user.otp == int(otp) and is_otp_valid(user.otp_created_at):
            user.email_verified = True
            user.save()
            return ({"detail": "Email confirmed successfully."}, HTTP_200_OK)
        else:
            return (
                {"detail": "Unable to verify your email address with provided OTP."},
                HTTP_400_BAD_REQUEST,
            )
    except User.DoesNotExist:
        return ({"detail": "User not found."}, HTTP_404_NOT_FOUND)
    except ValueError:
        return ({"detail": "Invalid user ID."}, HTTP_400_BAD_REQUEST)


def send_reset_otp(request: HttpRequest) -> tuple[dict, int]:
    email = request.data.get("email")
    if not email:
        return ({"detail": "Missing email."}, HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email=email)
        otp = randint(1000, 9999)
        user.otp = otp
        user.save()

        subject = "Your reset OTP on {0}".format(current_site)
        html_message = constant.create_otp_template(
                f"{user.first_name} {user.last_name}", otp, user.email
            )
        celery_tasks.send_email_task.delay(user.id,  subject, html_message)

        return ({"detail": "Reset OTP sent successfully."}, HTTP_200_OK)
    except User.DoesNotExist:
        return ({"detail": "User not found."}, HTTP_404_NOT_FOUND)


def Login(request: HttpRequest) -> tuple[dict, int]:
    email = request.data.get("email")
    password = request.data.get("password")
    print(email, password)
    if not email or not password:
        return ({"message": "Email or Password missing"}, HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = None

    if user is not None and user.check_password(password):
        if not user.is_active:
            return (
                {"message": "Your account has been deactivated"},
                HTTP_403_FORBIDDEN,
            )

        if not user.email_verified:
            return (
                {"user_id": user.uuid, "message": "Please activate email"},
                HTTP_403_FORBIDDEN,
            )

        if not user.is_approved:
            return (
                {"user_id": user.uuid, "message": "Please wait until admin approve your account"},
                HTTP_403_FORBIDDEN,
            )

        refresh = RefreshToken.for_user(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        django_login(request, user, backend="django.contrib.auth.backends.ModelBackend")

        return (
            {"user": OutputSerializers.LoginUserSerializer(user).data, "tokens": data},
            HTTP_200_OK,
        )
    # check if email not exist
    elif user is None:
        return ({"message": "Email not found"}, HTTP_401_UNAUTHORIZED)

    else:
        return ({"message": "Email or Password Error"}, HTTP_401_UNAUTHORIZED)


def Logout(self, request: Request, *args: Any, **kwargs: Any) -> dict:  # type: ignore
    if self.request.data.get("all"):
        token: OutstandingToken
        for token in OutstandingToken.objects.filter(user=request.user):  # type: ignore
            _, _ = BlacklistedToken.objects.get_or_create(token=token)  # type: ignore
        return {"status": "OK, goodbye, all refresh tokens blacklisted"}
    refresh_token = self.request.data.get("refresh_token")
    token = RefreshToken(token=refresh_token)  # type: ignore
    token.blacklist()  # type: ignore
    logout(request)
    return {"status": "OK, goodbye"}


def choose_user_type(request: Request) -> tuple[dict, int]:
    params_serialzer = ParamsSerializers.ChooseUserTypeSerializer(
        data=request.data, context={"request": request}
    )
    if not params_serialzer.is_valid():
        return ({"status": "error", "error": params_serialzer.errors}, HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(uuid=params_serialzer.validated_data["user_id"])
    except User.DoesNotExist:
        return ({"status": "error", "error": "User not found"}, HTTP_400_BAD_REQUEST)

    target_user_type = params_serialzer.validated_data["user_type"]
    user.user_type = target_user_type
    if target_user_type == "vendor":
        user.is_approved = False
    user.save()

    return ({"status": "success"}, HTTP_200_OK)
