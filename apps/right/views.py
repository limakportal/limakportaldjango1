from .models import Right
from .serializer import RightSerializer
from rest_framework.authtoken.views import APIView
from rest_framework.response import Response
from rest_framework import status
# import logging


# Create your views here.


class RightAPIView(APIView):
    def get(self,request):
        rights = Right.objects.all().order_by('id')
        serializer = RightSerializer(rights,many=True)
        return Response(serializer.data)

    def post(self,request):
        # logger.error('Something went wrong!')
        serializer = RightSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            # return Response({"message":"Personel Eklendi","status":"201"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response({"message":serializer.errors,"status":"400"}, status=status.HTTP_400_BAD_REQUEST)


class RightDetails(APIView):

    def get_object(self,id):
        try:
            return Right.objects.get(id=id)
        except Right.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        right = self.get_object(id)
        serializer = RightSerializer(right)
        return Response(serializer.data)


    def put(self, request,id):
        right = self.get_object(id)
        serializer = RightSerializer(right, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        right = self.get_object(id)
        right.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
