from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PersonEducation
from .serializer import PersonEducationSerializer


class PersonEducationAPIView(APIView):
    def get(self,request):
        personEducation = PersonEducation.objects.all().order_by('id')
        serializer = PersonEducationSerializer(personEducation,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = PersonEducationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonEducationDetails(APIView):

    def get_object(self,id):
        try:
            return PersonEducation.objects.get(id=id)
        except PersonEducation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        personEducation = self.get_object(id)
        serializer = PersonEducationSerializer(personEducation)
        return Response(serializer.data)


    def put(self, request,id):
        personEducation = self.get_object(id)
        serializer = PersonEducationSerializer(personEducation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        personEducation = self.get_object(id)
        personEducation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





