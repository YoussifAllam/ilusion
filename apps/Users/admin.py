from django.contrib import admin
# from . models import User #, Video, FavoriteVideos
# # Register your models here.
# admin.site.register(User)
# # admin.site.register(Video)
# # admin.site.register(FavoriteVideos)

from django.contrib.auth.models import Group, User
# from rest_framework.authtoken.models import Token
# from django_celery_beat.models import PeriodicTask, CrontabSchedule  # Example if using django-celery-beat

# Unregister models from Django admin
admin.site.unregister(Group)
# admin.site.unregister(User)
# admin.site.unregister(Token)

# If you are using django-celery-beat and want to unregister its models
# admin.site.unregister(PeriodicTask)
# admin.site.unregister(CrontabSchedule)

from django.contrib import admin
from django.contrib.auth.models import Group, User
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from allauth.account.models import EmailAddress
from rest_framework.authtoken.models import TokenProxy

# Check if the models are registered
if admin.site.is_registered(Group):
    admin.site.unregister(Group)

if admin.site.is_registered(User):
    admin.site.unregister(User)

if admin.site.is_registered(TokenProxy):
    admin.site.unregister(TokenProxy)

if admin.site.is_registered(BlacklistedToken):
    admin.site.unregister(BlacklistedToken)

if admin.site.is_registered(OutstandingToken):
    admin.site.unregister(OutstandingToken)

if admin.site.is_registered(EmailAddress):
    admin.site.unregister(EmailAddress)
