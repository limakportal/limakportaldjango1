from .models import Permission
from .serializer import PermissionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class PermissionAPIView(APIView):
    def get(self,request):
        permissions = Permission.objects.all().order_by('id')
        serializer = PermissionSerializer(permissions,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = PermissionSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PermissionDetails(APIView):

    def get_object(self,id):
        try:
            return Permission.objects.get(id=id)
        except Permission.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        permission = self.get_object(id)
        serializer = PermissionSerializer(permission)
        return Response(serializer.data)


    def put(self, request,id):
        permission = self.get_object(id)
        serializer = PermissionSerializer(permission, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        permission = self.get_object(id)
        permission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
