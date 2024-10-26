from django.contrib import admin
from .models import *
# # Register your models here.
from import_export.admin import ImportExportModelAdmin
from .resources import MyModelResource

class NotesInline(admin.TabularInline):
    model = Notes_model
    extra = 1

class Qr_code_image(admin.TabularInline):
    model = User_Qr_Code_image
    extra = 1

@admin.register(User_model)
class User_model_Admin(ImportExportModelAdmin):
    list_display = ('name' , 'memberShip_number' , 'memberShip_fk', 'phone', 'email' , 
        'bills_this_month', 'total_bills', 'total_amount_this_month',
          'total_amount_all_time' )
    
    list_filter = ('memberShip_fk',)
    exclude = ('memberShip_number',)
    inlines = [ Qr_code_image , NotesInline ]

    search_fields = ('memberShip_number',)
    # sortable_by = ('memberShip_number', 'bills_this_month', 'total_bills', 'total_amount_this_month', 'total_amount_all_time')
    ordering = ('memberShip_number',)
    resource_class = MyModelResource


admin.site.register(MemberShip_model)

@admin.register(Bills_model)
class Bills_model_Admin(admin.ModelAdmin):
    list_display = ('user_fk','amount', 'date' , 'serial_number')
    search_fields = ( 'serial_number' , 'date')
    # list_filter = ('user_fk',)


