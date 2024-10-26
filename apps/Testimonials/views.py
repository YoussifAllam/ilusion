from .serializers import *
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework import status  
from .models import *
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
User = get_user_model()


@api_view(['GET'])
def Get_Testimonials(request):
    testimonials = Testimonials.objects.all()
    serializer = GetTestimonialSerializer(testimonials, many=True)
    return Response({
        'status': 'success',
        'data': serializer.data
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_Testimonial(request):
    content = request.data.get('content')
    Target_user = request.user
    Target_date = {
        'user': Target_user.id,
        'user_name' : Target_user.name,
        'content' : content , 
    }
    serializer = ADDTestimonialSerializer(data=Target_date)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_reply(request):
    content = request.data.get('content')
    testimonial_id = request.data.get('Testimonial_id')
    target_user = request.user

    try:
        testimonial = Testimonials.objects.get(id=testimonial_id)
    except Testimonials.DoesNotExist:
        return Response({"detail": "Testimonial not found."}, status=status.HTTP_404_NOT_FOUND)

    target_data = {
        'Testimonial': testimonial.id,
        'user' : target_user.id,
        'user_name': target_user.username,
        'content': content,
    }
    serializer = RepliesSerializer(data=target_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)