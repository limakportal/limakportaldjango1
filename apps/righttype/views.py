from .models import RightType
from .serializer import RightTypeSerializer
from rest_framework.authtoken.views import APIView
from rest_framework.response import Response
from rest_framework import status


class RightTypeAPIView(APIView):
    def get(self,request):
        righttypes = RightType.objects.all().order_by('id')
        serializer = RightTypeSerializer(righttypes,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = RightTypeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RightTypeDetails(APIView):

    def get_object(self,id):
        try:
            return RightType.objects.get(id=id)
        except RightType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        righttype = self.get_object(id)
        serializer = RightTypeSerializer(righttype)
        return Response(serializer.data)


    def put(self, request,id):
        righttype = self.get_object(id)
        serializer = RightTypeSerializer(righttype, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        righttype = self.get_object(id)
        righttype.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
