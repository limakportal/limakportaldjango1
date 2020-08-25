from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
import json


from ..role.models import Role

from ..role.serializer import RoleSerializer , RoleViewSerializer
from ..authority.serializer import AuthoritySerializer
from ..userrole.serializer import UserRoleSerializer

class RoleWithPermissionAPIView(APIView):
    def get(self,request):
        roles = Role.objects.all()
        serializer = RoleViewSerializer(roles ,many = True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self,request): 
        transactionSaveId = transaction.savepoint()
        roleSerializer = RoleSerializer(data = request.data['role'])
        if roleSerializer.is_valid():
            roleSerializer.save()
            permissionRequestData = {}
            permissionRequestData = request.data['permissions']
            if len(permissionRequestData) > 0:
                for permissionData in permissionRequestData:
                    if 'id' in json.loads(json.dumps(permissionData)):
                        data = {}
                        data['Role'] = roleSerializer.data['id']
                        data['Permission'] = permissionData['id']
                        data['Active'] = 1   
                        authoritySerializer = AuthoritySerializer(data = data)
                        if authoritySerializer.is_valid():
                            authoritySerializer.save()
                        else:
                            transaction.savepoint_rollback(transaction)
                            return Response(authoritySerializer.error_messages , status = status.HTTP_400_BAD_REQUEST)
            accountRequestData = {}
            accountRequestData = request.data['users']
            if len(accountRequestData) > 0:
                for accountData in accountRequestData:
                    if 'id' in json.loads(json.dumps(accountData)):
                        data = {}
                        data['Role'] = roleSerializer.data['id']
                        data['Account'] = accountData['id']
                        userRoleSerializer = UserRoleSerializer(data = data)
                        if userRoleSerializer.is_valid():
                            userRoleSerializer.save()
                        else:
                            transaction.savepoint_rollback(transaction)
                            return Response(userRoleSerializer.error_messages , status = status.HTTP_400_BAD_REQUEST)
            return Response(roleSerializer.data, status=status.HTTP_201_CREATED)
        else:
            transaction.savepoint_rollback(transaction)
            return Response(roleSerializer.error_messages , status = status.HTTP_400_BAD_REQUEST)

class RoleWithPermissionDetails(APIView):
    def get_object(self,id):
        try:
            return Role.objects.get(id=id)
        except Role.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        role = self.get_object(id)
        serializer = RoleViewSerializer(role)
        return Response(serializer.data)
        

