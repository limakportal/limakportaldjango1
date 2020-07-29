from .models import District
from .serializer import DistrictSerializer
from rest_framework.authtoken.views import APIView
from rest_framework.response import Response
from rest_framework import status
# import logging


# Create your views here.


class DistrictAPIView(APIView):
    def get(self,request):
        districts = District.objects.all().order_by('id')
        serializer = DistrictSerializer(districts,many=True)
        return Response(serializer.data)

    def post(self,request):
        # logger.error('Something went wrong!')
        serializer = DistrictSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            # return Response({"message":"Personel Eklendi","status":"201"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response({"message":serializer.errors,"status":"400"}, status=status.HTTP_400_BAD_REQUEST)


class DistrictDetails(APIView):

    def get_object(self,id):
        try:
            return District.objects.get(id=id)
        except District.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        district = self.get_object(id)
        serializer = DistrictSerializer(district)
        return Response(serializer.data)


    def put(self, request,id):
        district = self.get_object(id)
        serializer = DistrictSerializer(district, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        district = self.get_object(id)
        district.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
