from .models import RightMainType
from .serializer import RightMainTypeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class RightMainTypeAPIView(APIView):
    def get(self,request):
        rightmaintypes = RightMainType.objects.all().order_by('id')
        serializer = RightMainTypeSerializer(rightmaintypes,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = RightMainTypeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RightMainTypeDetails(APIView):

    def get_object(self,id):
        try:
            return RightMainType.objects.get(id=id)
        except RightMainType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        rightmaintype = self.get_object(id)
        serializer = RightMainTypeSerializer(rightmaintype)
        return Response(serializer.data)


    def put(self, request,id):
        rightmaintype = self.get_object(id)
        serializer = RightMainTypeSerializer(rightmaintype, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        rightmaintype = self.get_object(id)
        rightmaintype.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
