from .models import RightLeave
from .serializer import RightLeaveSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class RightLeaveAPIView(APIView):
    def get(self,request):
        rightleaves = RightLeave.objects.all().order_by('id')
        serializer = RightLeaveSerializer(rightleaves,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = RightLeaveSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RightLeaveDetails(APIView):

    def get_object(self,id):
        try:
            return RightLeave.objects.get(id=id)
        except RightLeave.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        rightleave = self.get_object(id)
        serializer = RightLeaveSerializer(rightleave)
        return Response(serializer.data)


    def put(self, request,id):
        rightleave = self.get_object(id)
        serializer = RightLeaveSerializer(rightleave, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        rightleave = self.get_object(id)
        rightleave.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
