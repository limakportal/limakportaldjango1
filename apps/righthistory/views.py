from .models import RightHistory
from .serializer import RightHistorySerializer
from rest_framework.authtoken.views import APIView
from rest_framework.response import Response
from rest_framework import status
# import logging


# Create your views here.


class RightHistoryAPIView(APIView):
    def get(self,request):
        righthistries = RightHistory.objects.all().order_by('id')
        serializer = RightHistorySerializer(righthistries,many=True)
        return Response(serializer.data)

    def post(self,request):
        # logger.error('Something went wrong!')
        serializer = RightHistorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            # return Response({"message":"Personel Eklendi","status":"201"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response({"message":serializer.errors,"status":"400"}, status=status.HTTP_400_BAD_REQUEST)


class RightHistoryDetails(APIView):

    def get_object(self,id):
        try:
            return RightHistory.objects.get(id=id)
        except RightHistory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        righthistory = self.get_object(id)
        serializer = RightHistorySerializer(righthistory)
        return Response(serializer.data)


    def put(self, request,id):
        righthistory = self.get_object(id)
        serializer = RightHistorySerializer(righthistory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        righthistory = self.get_object(id)
        righthistory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
