from .models import VocationDays
from .serializer import VocationDaysSerializer 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view
from django.db.models import Q
import datetime


class VocationAPIView(APIView):
    # @method_decorator(cache_page(60*60*2))
    def get(self,request):
        days = VocationDays.objects.all().order_by('DateDay')
        serializer = VocationDaysSerializer(days,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = VocationDaysSerializer(data = request.data)
        if serializer.is_valid():
            days = VocationDays.objects.filter(DateDay__date = serializer.validated_data['DateDay'].date())
            if len(days) > 0:
                return Response("Girilen tarihde tatil günü mevcuttur", status=status.HTTP_201_CREATED)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VocationDetails(APIView):
        def get_object(self,id):
            try:
                return VocationDays.objects.get(id=id)
            except VocationDays.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        def get(self, request, id):
            vocationDays = self.get_object(id)
            serializer = VocationDaysSerializer(vocationDays)
            return Response(serializer.data)


        def put(self, request,id):
            vocationDays = self.get_object(id)
            serializer = VocationDaysSerializer(vocationDays, data=request.data)
            if serializer.is_valid():
                days = VocationDays.objects.filter(~Q(id = id) & Q(DateDay__date = serializer.validated_data['DateDay'].date()))
                if len(days) > 0:
                   return Response("Girilen tarihde tatil günü mevcuttur", status=status.HTTP_201_CREATED)
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        def delete(self, request, id):
            days = self.get_object(id)
            days.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def VocationDaysByMonthh(request,month):
    try:
        vdays = VocationDays.objects.filter(DateDay__year = datetime.date.today().year, DateDay__month = month)
        serializer = VocationDaysSerializer(vdays,many=True)
        return Response(serializer.data)
    except:
        pass

