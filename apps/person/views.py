from .models import Person
from .serializer import PersonSerializer
from rest_framework.authtoken.views import APIView
from rest_framework.response import Response
from rest_framework import status
# import logging


# Create your views here.


class PersonAPIView(APIView):
    def get(self,request):
        persons = Person.objects.all().order_by('id')
        serializer = PersonSerializer(persons,many=True)
        return Response(serializer.data)

    def post(self,request):
        # logger.error('Something went wrong!')
        serializer = PersonSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            # return Response({"message":"Personel Eklendi","status":"201"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response({"message":serializer.errors,"status":"400"}, status=status.HTTP_400_BAD_REQUEST)


class PersonDetails(APIView):

    def get_object(self,id):
        try:
            return Person.objects.get(id=id)
        except Person.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        person = self.get_object(id)
        serializer = PersonSerializer(person)
        return Response(serializer.data)


    def put(self, request,id):
        person = self.get_object(id)
        serializer = PersonSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        person = self.get_object(id)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
