from .models import Role
from .serializer import RoleSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# import logging


# Create your views here.


class RoleAPIView(APIView):
    def get(self,request):
        roles = Role.objects.all().order_by('id')
        serializer = RoleSerializer(roles,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = RoleSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoleDetails(APIView):

    def get_object(self,id):
        try:
            return Role.objects.get(id=id)
        except Role.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        role = self.get_object(id)
        serializer = RoleSerializer(role)
        return Response(serializer.data)


    def put(self, request,id):
        role = self.get_object(id)
        serializer = RoleSerializer(role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        role = self.get_object(id)
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)