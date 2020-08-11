from .models import PersonelInformation
from .serializer import PersonelInformationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PersonelInformationAPIView(APIView):
    def get(self,request):
        personelinformations = PersonelInformation.objects.all().order_by('id')
        serializer = PersonelInformationSerializer(personelinformations,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = PersonelInformationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonelInformationDetails(APIView):

    def get_object(self,id):
        try:
            return PersonelInformation.objects.get(id=id)
        except PersonelInformation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        personelinformation = self.get_object(id)
        serializer = PersonelInformationSerializer(personelinformation)
        return Response(serializer.data)


    def put(self, request,id):
        personelinformation = self.get_object(id)
        serializer = PersonelInformationSerializer(personelinformation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        personelinformation = self.get_object(id)
        personelinformation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
