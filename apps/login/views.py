from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from apps.account.models import Account
from apps.account.serializer import AccountSerializer
from apps.person.models import Person
from apps.person.serializer import PersonSerializer
from apps.staff.models import Staff
from apps.staff.serializer import StaffSerializer
from apps.authority.models import Authority
from apps.authority.serializer import AuthoritySerializer
from rest_framework import status




class HelloView(APIView):
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class GoogleView(APIView):
    def post(self, request):
        payload = {'access_token': request.data.get("token")}  # validate the token
        r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        data = json.loads(r.text)

        if 'error' in data:
            content = {'message': 'Hatalı google hesabı yada hatalı google access token.'}
            return Response(content)

        try:
            accounts = Account.objects.get(email=data['email'])
            person =Person.objects.get(Email=data['email'])
            staff = Staff.objects.get(Person=person.id)
            authority=Authority.objects.filter(Role=staff.Role)          
            userSerializer = AccountSerializer(accounts)
            authoritySerializer=AuthoritySerializer(authority,many=True)
            token = RefreshToken.for_user(accounts) 
            response = {}
            response['User'] = userSerializer.data
            response['Authority'] = authoritySerializer.data
            response['access_token'] = str(token.access_token)
            # response['refresh_token'] = str(token)
            return Response(response,status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            content = {'message': 'Kayıtlı kullanıcı bulunamadı'}
            return Response(content,status=status.HTTP_401_UNAUTHORIZED)