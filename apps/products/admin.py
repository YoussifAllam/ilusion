from django.contrib import admin
from .models import *
from .forms import ProductImagesForm
# Register your models here.


admin.site.site_header  = 'Agave World Admin Panel'
admin.site.site_title  = 'Agave World Admin Panel'

class ProductsPhotoInline(admin.StackedInline):  # Or admin.StackedInline for a different layout
    model = ProductImages
    form = ProductImagesForm
    extra = 1  # Number of empty forms to display

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1

class ProductsAdmin(admin.ModelAdmin):
    inlines = [ProductsPhotoInline , ProductSizeInline]
    list_display = ('Product_name', 'IS_spacial_product','price_range')  
    list_filter = ('Product_category',) 
    search_fields = ('Product_name' , )  
    list_editable = ('IS_spacial_product',)


class rateingsAdmin(admin.ModelAdmin):
    list_display = ('Targer_Product', 'User_Name','Rating_stars')
    




from django.contrib.auth.models import Group
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from allauth.account.models import EmailAddress
from rest_framework.authtoken.models import TokenProxy
admin.site.register(Product_Rating , rateingsAdmin)
admin.site.register(Home_OurProducts )
admin.site.register(Products , ProductsAdmin)
admin.site.register(Category)

admin.site.unregister(TokenProxy)
admin.site.unregister(Group)
admin.site.unregister(BlacklistedToken)
admin.site.unregister(OutstandingToken)
admin.site.unregister(EmailAddress)