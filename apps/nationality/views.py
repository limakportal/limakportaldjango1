from .models import Nationality
from .serializer import NationalitySerializer
from rest_framework.authtoken.views import APIView
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