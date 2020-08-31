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
import requests

from ..organization.models import Organization
from ..organization.serializer import OrganizationTreeSerializer
from ..person.models import Person
from ..permission.models import Permission
from ..permission.views import PermissionSerializer
from ..userrole.models import UserRole

from ..businessrules.views import IsManager


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
            # person =Person.objects.get(Email=data['email'])
            # staff = Staff.objects.get(Person=person.id)
            # authority=Authority.objects.filter(Role=staff.Role)          
            userSerializer = AccountSerializer(accounts)
            # authoritySerializer=AuthoritySerializer(authority,many=True)
            token = RefreshToken.for_user(accounts) 
            response = {}
            # response['User'] = userSerializer.data
            # response['Authority'] = authoritySerializer.data
            # response['access_token'] = str(token.access_token)
            # response['refresh_token'] = str(token)


            response['token'] = str(token.access_token)
            response['access_token'] = str(token.access_token)
            responseUser = {}
            responseUser['id'] = userSerializer.data['id']
            responseUser['Email'] = data['email']
            response['User'] = responseUser



            try:
                person = Person.objects.get(Email = data['email'])
                responsePerson = {}
                responsePerson['id'] = person.id
                responsePerson['Name'] = person.Name
                responsePerson['Surname'] = person.Surname
                response['Person'] = responsePerson
            except :
                response['Person'] = None
                requestIsManager = None

        


            allPermissions = []
            userRoles = UserRole.objects.filter(Account_id = userSerializer.data['id'])
            for userRole in userRoles:
                authorityes = Authority.objects.filter(Role_id = userRole.Role_id , Active = True)
                for authority in authorityes:
                    permissions = Permission.objects.filter(id = authority.Permission_id)
                    for permission in permissions:

                        allPermissions.append(permission);    

            response['permissions'] = PermissionSerializer(allPermissions, many=True).data
            if response['Person'] != None:
                response['IsManager'] = IsManager(person.id)
            else:
                response['IsManager'] = None

            
            return Response(response,status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            content = {'message': 'Kayıtlı kullanıcı bulunamadı'}
            return Response(content,status=status.HTTP_401_UNAUTHORIZED)