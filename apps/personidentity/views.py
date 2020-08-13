from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PersonIdentity
from .serializer import PersonIdentitySerializer


class PersonIdentityAPIView(APIView):
    def get(self,request):
        personIdentity = PersonIdentity.objects.all().order_by('id')
        serializer = PersonIdentitySerializer(personIdentity,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = PersonIdentitySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonIdentityDetails(APIView):

    def get_object(self,id):
        try:
            return PersonIdentity.objects.get(id=id)
        except PersonIdentity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        personIdentity = self.get_object(id)
        serializer = PersonIdentitySerializer(personIdentity)
        return Response(serializer.data)


    def put(self, request,id):
        personIdentity = self.get_object(id)
        serializer = PersonIdentitySerializer(personIdentity, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        personIdentity = self.get_object(id)
        personIdentity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





