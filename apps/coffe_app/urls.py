from django.urls import path
from .views import *

urlpatterns = [
    path('coffe_users/', CoffeUsersView.as_view()),
]