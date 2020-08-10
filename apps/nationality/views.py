from .models import Nationality
from .serializer import NationalitySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class NationalityAPIView(APIView):
    def get(self,request):
        nationalities = Nationality.objects.all().order_by('id')
        serializer = NationalitySerializer(nationalities,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = NationalitySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NationalityDetails(APIView):

    def get_object(self,id):
        try:
            return Nationality.objects.get(id=id)
        except Nationality.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        nationality = self.get_object(id)
        serializer = NationalitySerializer(nationality)
        return Response(serializer.data)


    def put(self, request,id):
        nationality = self.get_object(id)
        serializer = NationalitySerializer(nationality, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        nationality = self.get_object(id)
        nationality.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)