from .models import MaritalStatus
from .serializer import MaritalStatusSerializer
from rest_framework.views import APIView
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

class MaritalStatusDetails(APIView):

    def get_object(self,id):
        try:
            return MaritalStatus.objects.get(id=id)
        except MaritalStatus.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        maritalStatus = self.get_object(id)
        serializer = MaritalStatusSerializer(maritalStatus)
        return Response(serializer.data)


    def put(self, request,id):
        maritalStatus = self.get_object(id)
        serializer = MaritalStatusSerializer(maritalStatus, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        maritalStatus = self.get_object(id)
        maritalStatus.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)