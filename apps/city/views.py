from .models import City
from .serializer import CitySerializer , CityViewSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class CityAPIView(APIView):
    @method_decorator(cache_page(60*60*2))
    def get(self,request):
        cities = City.objects.all().order_by('Name')
        serializer = CityViewSerializer(cities,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = CitySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CityDetails(APIView):

    def get_object(self,id):
        try:
            return City.objects.get(id=id)
        except City.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @method_decorator(cache_page(60*60*2))
    def get(self, request, id):
        city = self.get_object(id)
        serializer = CityViewSerializer(city)
        return Response(serializer.data)


    def put(self, request,id):
        city = self.get_object(id)
        serializer = CitySerializer(city, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        city = self.get_object(id)
        city.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
