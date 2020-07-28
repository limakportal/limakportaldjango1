from .models import PersonHistory
from .serializer import PersonHistorySerializer
from rest_framework.authtoken.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PersonHistoryAPIView(APIView):
    def get(self,request):
        personhistories = PersonHistory.objects.all().order_by('id')
        serializer = PersonHistorySerializer(personhistories,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = PersonHistorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonHistoryDetails(APIView):

    def get_object(self,id):
        try:
            return PersonHistory.objects.get(id=id)
        except PersonHistory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        personhistory = self.get_object(id)
        serializer = PersonHistorySerializer(personhistory)
        return Response(serializer.data)


    def put(self, request,id):
        personhistory = self.get_object(id)
        serializer = PersonHistorySerializer(personhistory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        personhistory = self.get_object(id)
        personhistory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
