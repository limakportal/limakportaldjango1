from .models import MaritalStatus
from .serializer import MaritalStatusSerializer
from rest_framework.authtoken.views import APIView
from rest_framework.response import Response
from rest_framework import status

class MaritalStatusAPIView(APIView):
    def get(self,request):
        maritalStatuses = MaritalStatus.objects.all().order_by('id')
        serializer = MaritalStatusSerializer(maritalStatuses,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = MaritalStatusSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)