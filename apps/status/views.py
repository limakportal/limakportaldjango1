from .models import Status
from .serializer import StatusSerializer
from rest_framework.views import APIView
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

class StatusDetails(APIView):
        def get_object(self,id):
            try:
                return Status.objects.get(id=id)
            except Status.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        def get(self, request, id):
            status = self.get_object(id)
            serializer = StatusSerializer(status)
            return Response(serializer.data)


        def put(self, request,id):
            status = self.get_object(id)
            serializer = StatusSerializer(status, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        def delete(self, request, id):
            status = self.get_object(id)
            status.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

