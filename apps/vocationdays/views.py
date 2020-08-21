from .models import VocationDays
from .serializer import VocationDaysSerializer 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class VocationAPIView(APIView):
    @method_decorator(cache_page(60*60*2))
    def get(self,request):
        days = VocationDays.objects.all().order_by('DateDay')
        serializer = VocationDaysSerializer(days,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = VocationDaysSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


