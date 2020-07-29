from .models import Title
from .serializer import TitleSerializer
from rest_framework.authtoken.views import APIView
from rest_framework.response import Response
from rest_framework import status


class TitleAPIView(APIView):
    def get(self,request):
        titles = Title.objects.all().order_by('id')
        serializer = TitleSerializer(titles,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = TitleSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TitleDetails(APIView):

    def get_object(self,id):
        try:
            return Title.objects.get(id=id)
        except Title.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        title = self.get_object(id)
        serializer = TitleSerializer(title)
        return Response(serializer.data)


    def put(self, request,id):
        title = self.get_object(id)
        serializer = TitleSerializer(title, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        title = self.get_object(id)
        title.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
