from django.contrib import admin
from . import models as app_models
from image_uploader_widget.widgets import ImageUploaderWidget
from django.db import models


@admin.register(app_models.DrinkMenu)
class drinkMenuAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ImageField: {'widget': ImageUploaderWidget},
    }


@admin.register(app_models.FoodMenu)
class FoodMenuAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ImageField: {'widget': ImageUploaderWidget},
    }


@admin.register(app_models.DailyPromo)
class promoMenuAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ImageField: {'widget': ImageUploaderWidget},
    }


@admin.register(app_models.WeeklyEvents)
class eventsMenuAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ImageField: {'widget': ImageUploaderWidget},
    }


@admin.register(app_models.ClubMembers)
class clubMenuAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ImageField: {'widget': ImageUploaderWidget},
    }


@admin.register(app_models.LoyaltyProgram)
class loyaltyMenuAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ImageField: {'widget': ImageUploaderWidget},
    }


admin.site.register(app_models.Complains)
admin.site.register(app_models.Rates)
