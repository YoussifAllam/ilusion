from rest_framework.serializers import ( # noqa
    ModelSerializer,
)
from .. import models


class FoodMenuSerializer(ModelSerializer):
    class Meta:
        model = models.FoodMenu
        fields = '__all__'


class DrinkMenuSerializer(ModelSerializer):
    class Meta:
        model = models.DrinkMenu
        fields = '__all__'


class DailyPromoSerializer(ModelSerializer):
    class Meta:
        model = models.DailyPromo
        fields = '__all__'


class WeeklyEventsSerializer(ModelSerializer):
    class Meta:
        model = models.WeeklyEvents
        fields = '__all__'


class ClubMembersSerializer(ModelSerializer):
    class Meta:
        model = models.ClubMembers
        fields = '__all__'


class LoyaltyProgramSerializer(ModelSerializer):
    class Meta:
        model = models.LoyaltyProgram
        fields = '__all__'


class ComplainsSerializer(ModelSerializer):
    class Meta:
        model = models.Complains
        fields = '__all__'


class RatesSerializer(ModelSerializer):
    class Meta:
        model = models.Rates
        fields = '__all__'