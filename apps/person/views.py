from .models import Personel
from .serializer import PersonelSerializer
from rest_framework.authtoken.views import APIView
from rest_framework.response import Response
from rest_framework import status
# import logging


# Create your views here.

class PersonelAPIView(APIView):
    def get(self,request):
        personels = Personel.objects.all().order_by('id')
        serializer = PersonelSerializer(personels,many=True)
        return Response(serializer.data)

    def post(self,request):
        # logger.error('Something went wrong!')
        serializer = PersonelSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"message":"Personel Eklendi","status":"201"}, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":serializer.errors,"status":"400"}, status=status.HTTP_400_BAD_REQUEST)


class PersonelDetails(APIView):

    def get_object(self,id):
        try:
            return Personel.objects.get(id=id)
        except Personel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        personel = self.get_object(id)
        serializer = PersonelSerializer(personel)
        return Response(serializer.data)


    def put(self, request,id):
        personel = self.get_object(id)
        serializer = PersonelSerializer(personel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        personel = self.get_object(id)
        personel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
