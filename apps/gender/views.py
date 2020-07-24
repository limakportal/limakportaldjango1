from .models import Gender
from .serializer import GenderSerializer
from rest_framework.authtoken.views import APIView
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
        # logger.error('Something went wrong!')
        serializer = GenderSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            # return Response({"message":"Personel Eklendi","status":"201"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response({"message":serializer.errors,"status":"400"}, status=status.HTTP_400_BAD_REQUEST)