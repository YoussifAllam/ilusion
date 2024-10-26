from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED  # noqa
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import OutputSerializers
from . import models


class food_menu(APIView):
    def get(self, request):
        data = models.FoodMenu.objects.all()
        serializer = OutputSerializers.FoodMenuSerializer(data, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data
        }, HTTP_200_OK)


class Drinkmenu(APIView):
    def get(self, request):
        data = models.DrinkMenu.objects.all()
        serializer = OutputSerializers.DrinkMenuSerializer(data, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data
        }, HTTP_200_OK)


class DailyPromo(APIView):
    def get(self, request):
        data = models.DailyPromo.objects.all()
        serializer = OutputSerializers.DailyPromoSerializer(data, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data
        }, HTTP_200_OK)


class WeeklyEvents(APIView):
    def get(self, request):
        data = models.WeeklyEvents.objects.all()
        serializer = OutputSerializers.WeeklyEventsSerializer(data, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data
        }, HTTP_200_OK)


class ClubMembers(APIView):
    def get(self, request):
        data = models.ClubMembers.objects.all()
        serializer = OutputSerializers.ClubMembersSerializer(data, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data
        }, HTTP_200_OK)


class LoyaltyProgram(APIView):
    def get(self, request):
        data = models.LoyaltyProgram.objects.all()
        serializer = OutputSerializers.LoyaltyProgramSerializer(
            data, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data
        }, HTTP_200_OK)


class ComplainsAPI(APIView):
    def post(self, request):
        serializer = OutputSerializers.ComplainsSerializer(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'data': serializer.data
            }, HTTP_201_CREATED)
        else:
            return Response({
                'status': 'failed',
                'data': serializer.errors
            }, HTTP_400_BAD_REQUEST)


class RatesAPI(APIView):
    def post(self, request):
        serializer = OutputSerializers.RatesSerializer(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'data': serializer.data
            }, HTTP_201_CREATED)
        else:
            return Response({
                'status': 'failed',
                'data': serializer.errors
            }, HTTP_400_BAD_REQUEST)

    def get(self, request):
        data = models.Rates.objects.all()
        serializer = OutputSerializers.RatesSerializer(data, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data
        }, HTTP_200_OK)
