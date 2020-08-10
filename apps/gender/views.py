from .models import Gender
from .serializer import GenderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# import logging


# Create your views here.


class GenderAPIView(APIView):
    def get(self,request):
        genders = Gender.objects.all().order_by('id')
        serializer = GenderSerializer(genders,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = GenderSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GenderDetails(APIView):

    def get_object(self,id):
        try:
            return Gender.objects.get(id=id)
        except Gender.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        gender = self.get_object(id)
        serializer = GenderSerializer(gender)
        return Response(serializer.data)


    def put(self, request,id):
        gender = self.get_object(id)
        serializer = GenderSerializer(gender, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        gender = self.get_object(id)
        gender.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)