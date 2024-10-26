from rest_framework.status import HTTP_200_OK , HTTP_400_BAD_REQUEST , HTTP_201_CREATED 
from rest_framework.response import Response
from rest_framework.views import APIView 
# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated 
from .serializers import InputSerializers , OutputSerializers , ParamsSerializers
# from .db_queries import selectors ,services
from .models import *
from django.utils import timezone

class CoffeUsersView(APIView):

    def get(self , request):
        
        serializer_class = ParamsSerializers.UserParamsSerializer(data = request.GET)
        if not serializer_class.is_valid():
            return Response(serializer_class.errors , status = HTTP_400_BAD_REQUEST)
        
        validate_data = serializer_class.validated_data
        user_id = validate_data['id']
        print('++++++' , user_id)

        try :
            user = User_model.objects.get(id = user_id)
        except User_model.DoesNotExist:
            return Response({'status':'fial', 'error':'user not sound'} , HTTP_400_BAD_REQUEST)
        serializer = OutputSerializers.UserSerializer(user )
        return Response({
            'status' : 'success' , 'data' : serializer.data
            } , status = HTTP_200_OK
        )

    def post(self , request):
        serializer_class = ParamsSerializers.BillSerializer(data = request.data)
        if not serializer_class.is_valid():
            return Response(serializer_class.errors , status = HTTP_400_BAD_REQUEST)
        
        validate_data = serializer_class.validated_data
        validate_data['user_fk'] = validate_data['user_id']
        del validate_data['user_id']

        validate_data['date'] = timezone.now()

        create_serizlizer = InputSerializers.BillsSerializer(data = validate_data)
        if create_serizlizer.is_valid():
            create_serizlizer.save()
        else  :
            return Response(
                {'status' : 'failed' , 'error' : create_serizlizer.errors} , 
                status = HTTP_400_BAD_REQUEST
        )
        
        return Response(
            {'status' : 'success' , 'message' : 'Bill created successfully'},
            status = HTTP_201_CREATED
        )
    
