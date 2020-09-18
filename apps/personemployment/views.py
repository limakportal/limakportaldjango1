from .models import PersonEmployment
from .serializer import PersonEmploymentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..utils.enums import  EnumStatus

import datetime
import json


class PersonEmploymentAPIView(APIView):
    def get(self,request):
        personemployments = PersonEmployment.objects.all().order_by('id')
        serializer = PersonEmploymentSerializer(personemployments,many=True)
        return Response(serializer.data)

    def post(self,request):
        today = datetime.date.today()
        # if 'EndDate' in json.loads(json.dumps(request.data))
        enddate = request.data['EndDate']
        if enddate != None:
            enddate = datetime.datetime.strptime(request.data['EndDate'], '%Y-%m-%d')
        data = request.data
        
        if enddate == None or enddate.date() > today:
            data['Status'] = int(EnumStatus.Active)
        else:
            data['Status'] = int(EnumStatus.Passive)

        serializer = PersonEmploymentSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonEmploymentDetails(APIView):

    def get_object(self,id):
        try:
            return PersonEmployment.objects.get(id=id)
        except PersonEmployment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        personemployment = self.get_object(id)
        serializer = PersonEmploymentSerializer(personemployment)
        return Response(serializer.data)


    def put(self, request,id):
        personemployment = self.get_object(id)
        serializer = PersonEmploymentSerializer(personemployment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        personemployment = self.get_object(id)
        personemployment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
