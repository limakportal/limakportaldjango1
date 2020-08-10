from .models import OrganizationType
from .serializer import OrganizationTypeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class OrganizationTypeAPIView(APIView):
    def get(self,request):
        organizationtypes = OrganizationType.objects.all().order_by('id')
        serializer = OrganizationTypeSerializer(organizationtypes,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = OrganizationTypeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizationTypeDetails(APIView):

    def get_object(self,id):
        try:
            return OrganizationType.objects.get(id=id)
        except OrganizationType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        organizationtype = self.get_object(id)
        serializer = OrganizationTypeSerializer(organizationtype)
        return Response(serializer.data)


    def put(self, request,id):
        organizationtype = self.get_object(id)
        serializer = OrganizationTypeSerializer(organizationtype, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        organizationtype = self.get_object(id)
        organizationtype.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
