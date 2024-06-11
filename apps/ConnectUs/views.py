from django.core.mail import send_mail
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status  
# Create your views here.


@api_view(['POST'])
def send_email(request):
    subject = request.data.get('subject')
    message=request.data.get('message')
    email = request.data.get('email')
    name = request.data.get('name')
    
    if not subject or not message or not email or not name:
        return Response({"detail": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

    subject = f'You have a new message from MyAgaveWorld.com'
    message = f"""
    My Name : {name}
    My Email : {email}
    Subject : {subject}
    Message : {message}
    """
    send_mail(subject, message , email, ['youssifhassan011@gmail.com'])  # Use Django's send_mail
    return Response({"detail": "Email sent successfully"}, status=status.HTTP_200_OK)
    