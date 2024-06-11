from django.urls import path 
from .views import *
urlpatterns = [
    path('Get_Testimonials/', Get_Testimonials),
    path('add_Testimonial/' , add_Testimonial) , 
    path('add_reply/' , add_reply)
]
