from .models import Staff
from .serializer import StaffSerializer , StaffJoinSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class StaffAPIView(APIView):
    def get(self,request):
        staff = Staff.objects.all().order_by('id')
        serializer = StaffJoinSerializer(staff,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = StaffSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaffDetails(APIView):

    def get_object(self,id):
        try:
            return Staff.objects.get(id=id)
        except Staff.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        staff = self.get_object(id)
        serializer = StaffSerializer(staff)
        return Response(serializer.data)


    def put(self, request,id):
        staff = self.get_object(id)
        serializer = StaffSerializer(staff, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        staff = self.get_object(id)
        staff.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
