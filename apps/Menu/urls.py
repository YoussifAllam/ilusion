from django.urls import path
from . import views

urlpatterns = [
    path('food_menu/', views.food_menu.as_view()),
    path('drink_menu/', views.Drinkmenu.as_view()),
    path('DailyPromo/', views.DailyPromo.as_view()),
    path('WeeklyEvents/', views.WeeklyEvents.as_view()),
    path('ClubMembers/', views.ClubMembers.as_view()),
    path('LoyaltyProgram/', views.LoyaltyProgram.as_view()),
    path('Complains/', views.ComplainsAPI.as_view()),
    path('Rates/', views.RatesAPI.as_view())


]
