from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import StaffHistory
from .serializer import StaffHistorySerializer


class StaffHistoryAPIView(APIView):
    def get(self, request):
        staffHistory = StaffHistory.objects.all()
        serializer = StaffHistorySerializer(staffHistory, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StaffHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaffHistoryDetails(APIView):
    def get_object(self, id):
        try:
            return StaffHistory.objects.get(id=id)
        except StaffHistory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        staffHistory = self.get_object(id)
        serializer = StaffHistorySerializer(staffHistory)
        return Response(serializer.data)

    def put(self, request, id):
        staffHistory = self.get_object(id)
        serializer = StaffHistorySerializer(staffHistory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        staffHistory = self.get_object(id)
        staffHistory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
