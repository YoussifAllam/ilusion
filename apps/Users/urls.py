from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView 
app_name = 'Users'
router = DefaultRouter()
router.register(r'users', UserViewSet,basename='users') 

urlpatterns = [
    
    path('', include(router.urls)),
    path('user/login/', CustomTokenObtainPairView.as_view(), name='user-login'),
    
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('userinfo/', current_user,name='user_info'), 
    path('userinfo/update/', update_user,name='update_user'), 
    
    path('forgot_password/', forgot_password,name='forgot_password'), 
    path('reset_password/<str:token>',reset_password,name='reset_password'), 
    
    path('user/logout/', APILogoutView.as_view(), name='logout_token'),
    

]