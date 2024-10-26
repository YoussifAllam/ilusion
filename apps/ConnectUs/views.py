from django.core.mail import send_mail, BadHeaderError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings 
# Create your views here.


@api_view(['POST'])
def send_email(request):
    subject = request.data.get('subject')
    message = request.data.get('message')
    email = request.data.get('email')
    name = request.data.get('name')
    
    if not subject or not message or not email or not name:
        return Response({"detail": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

    full_subject = 'You have a new message from MyAgaveWorld.com'
    full_message = f"""
    My Name : {name}
    My Email : {email}
    Subject : {subject}
    Message : {message}
    """

    try:
        send_mail(full_subject, full_message, settings.DEFAULT_FROM_EMAIL, ['youssifhassan011@gmail.com'])
    except BadHeaderError:
        return Response({"detail": "Invalid header found."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"detail": "Email sent successfully"}, status=status.HTTP_200_OK)