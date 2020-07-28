import jwt
from .models import User
from .serializer import UserSerializer
from rest_framework.authtoken.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_jwt.serializers import jwt_payload_handler
from django_project import settings
from django.contrib.auth.signals import user_logged_in

@api_view(['POST'])
@permission_classes([AllowAny, ])
def Login(request):
 
    try:
        email = request.data['Email']
        password = request.data['Password']
 
        user = User.objects.get(Email=email, Password=password)
        if user:
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {}
                user_details['name'] = "%s %s" % (
                    user.first_name, user.last_name)
                user_details['token'] = token
                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)
 
            except Exception as e:
                raise e
        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'please provide a email and a password'}
        return Response(res)

    