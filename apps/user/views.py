from .models import User
from .serializer import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def Login(request):
 
    try:
        email = request.data['Email']
        password = request.data['Password']
 
        user = User.objects.get(Email=email, Password=password)
        if user:
            try:
                return Response(user, status=status.HTTP_200_OK)
 
            except Exception as e:
                raise e
        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError as e:
        res = {'error': e}
        return Response(res)

    