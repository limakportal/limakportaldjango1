from .models import Organization
from .serializer import OrganizationSerializer , OrganizationTreeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class OrganizationAPIView(APIView):
    def get(self,request):
        organizations = Organization.objects.all().order_by('id')
        serializer = OrganizationSerializer(organizations,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = OrganizationSerializer(data = request.data)
        if serializer.is_valid():
            organization = Organization.objects.filter(UpperOrganization = request.data['UpperOrganization'], Name = request.data['Name'])
            if len(organization):
                return Response('Bu birimde aynı isimli organizasyon tanımlıdır.',status=status.HTTP_404_NOT_FOUND)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrganizationTreeList(APIView):
    def get(self,request):
        organizations = Organization.objects.filter(UpperOrganization=None)
        serializer = OrganizationTreeSerializer(organizations,many=True)
        return Response(serializer.data)


class OrganizationDetails(APIView):

    def get_object(self,id):
        try:
            return Organization.objects.get(id=id)
        except Organization.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        organization = self.get_object(id)
        serializer = OrganizationSerializer(organization)
        return Response(serializer.data)


    def put(self, request,id):
        organization = self.get_object(id)
        serializer = OrganizationSerializer(organization, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        organization = self.get_object(id)
        organization.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
