from .models import AnnouncmentOrganization
from .serializer import AnnouncmentOrganizationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class AnnouncmentOrganizationAPIView(APIView):
    def get(self,request):
        announcmentorganizations = AnnouncmentOrganization.objects.all().order_by('id')
        serializer = AnnouncmentOrganizationSerializer(announcmentorganizations,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = AnnouncmentOrganizationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnnouncmentOrganizationDetails(APIView):

    def get_object(self,id):
        try:
            return AnnouncmentOrganization.objects.get(id=id)
        except AnnouncmentOrganization.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        announcmentorganization = self.get_object(id)
        serializer = AnnouncmentOrganizationSerializer(announcment)
        return Response(serializer.data)


    def put(self, request,id):
        announcmentorganization = self.get_object(id)
        serializer = AnnouncmentOrganizationSerializer(announcmentorganization, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        announcmentorganization = self.get_object(id)
        announcmentorganization.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)