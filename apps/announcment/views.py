from .models import Announcment
from .serializer import AnnouncmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class AnnouncmentAPIView(APIView):
    def get(self,request):
        announcments = Announcment.objects.all().order_by('id')
        serializer = AnnouncmentSerializer(announcments,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = AnnouncmentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnnouncmentDetails(APIView):

    def get_object(self,id):
        try:
            return Announcment.objects.get(id=id)
        except Announcment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        announcment = self.get_object(id)
        serializer = AnnouncmentSerializer(announcment)
        return Response(serializer.data)


    def put(self, request,id):
        announcment = self.get_object(id)
        serializer = AnnouncmentSerializer(announcment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        announcment = self.get_object(id)
        announcment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)