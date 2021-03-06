from .models import RightStatus
from .serializer import RightStatusSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class RightStatusAPIView(APIView):
    def get(self,request):
        rightstatuses = RightStatus.objects.all().order_by('id')
        serializer = RightStatusSerializer(rightstatuses,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = RightStatusSerializer(data = request.data)
        if serializer.is_valid():
            if request.data['Name'] == "":
                return Response('İzin durum adı boş olamaz.',status=status.HTTP_404_NOT_FOUND)
            rightstatuses = RightStatus.objects.filter(Name = request.data['Name'])
            if len(rightstatuses):
                return Response('İzin durumunda aynı isimli kayıt bulunmaktadır.',status=status.HTTP_404_NOT_FOUND)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RightStatusDetails(APIView):

    def get_object(self,id):
        try:
            return RightStatus.objects.get(id=id)
        except RightStatus.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        rightstatus = self.get_object(id)
        serializer = RightStatusSerializer(rightstatus)
        return Response(serializer.data)


    def put(self, request,id):
        rightstatus = self.get_object(id)
        serializer = RightStatusSerializer(rightstatus, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        rightstatus = self.get_object(id)
        rightstatus.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
