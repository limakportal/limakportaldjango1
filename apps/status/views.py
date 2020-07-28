from .models import Status
from .serializer import StatusSerializer
from rest_framework.authtoken.views import APIView
from rest_framework.response import Response
from rest_framework import status


class StatusAPIView(APIView):
    def get(self,request):
        status = Status.objects.all().order_by('id')
        serializer = StatusSerializer(status,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = StatusSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

