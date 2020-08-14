from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from .models import Person
from .serializer import PersonSerializer , PersonViewSerializer
from apps.personidentity.models import PersonIdentity
from apps.personidentity.serializer import PersonIdentitySerializer
from apps.personbusiness.models import PersonBusiness
from apps.personbusiness.serializer import PersonBusinessSerializer
from apps.personeducation.models import PersonEducation
from apps.personeducation.serializer import PersonEducationSerializer
from apps.personfamily.models import PersonFamily
from apps.personfamily.serializer import PersonFamilySerializer

class PersonAPIView(APIView):
    @permission_classes((IsAuthenticated, ))
    def get(self,request):
        persons = Person.objects.all().order_by('id')
        serializer = PersonSerializer(persons,many=True)
        return Response(serializer.data)

    def post(self,request):
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

class PersonWithPersonInformationAPIView(APIView):
    def get(self,request):
        persons = Person.objects.all().order_by('id')
        serializer = PersonViewSerializer(persons,many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self,request):

        transactionSaveId = transaction.savepoint()

        personSerializer = PersonSerializer(data = request.data['person'] )
        if personSerializer.is_valid():
            person = personSerializer.save()

            personIdentitySerializer = PersonIdentitySerializer(data = request.data['personIdentity'])   
            if len(request.data['personIdentity']) > 0 :
                personIdentitySerializer.initial_data['Person'] = person.id               
                if personIdentitySerializer.is_valid():
                    personIdentitySerializer.save()
                else:
                    transaction.savepoint_rollback(transactionSaveId)

            personbusinessSerializer = PersonBusinessSerializer(data = request.data['personbusiness'])
           
            if len(request.data['personbusiness']) > 0:
                personbusinessSerializer.initial_data['Person'] = person.id 
                if personbusinessSerializer.is_valid():
                    personbusinessSerializer.save()
                else:
                    transaction.savepoint_rollback(transactionSaveId)


            if len(request.data['personeducation']) > 0:
                for personEducation in request.data['personeducation']:
                    personEducationSerializer = PersonEducationSerializer(data=personEducation)
                    personEducationSerializer.initial_data['Person'] = person.id
                    if personEducationSerializer.is_valid():
                        personEducationSerializer.save()
                    else:
                        transaction.savepoint_rollback(transactionSaveId)

            if len(request.data['personfamily']) > 0:
                for personFamily in request.data['personfamily']:
                    personFamilySerializer = PersonFamilySerializer(data=personFamily)
                    personFamilySerializer.initial_data['Person'] = person.id
                    if personFamilySerializer.is_valid():
                        personFamilySerializer.save()
                    else:
                        transaction.savepoint_rollback(transactionSaveId)
            try:
                newPerson = Person.objects.get(id=person.id)
                serializer = PersonViewSerializer(newPerson)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)        
        else:                
            transaction.savepoint_rollback(transactionSaveId)

class PersonWithPersonInformationDetails(APIView):

    def get_object(self,id):
        try:
            return Person.objects.get(id=id)
        except Person.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        person = self.get_object(id)
        serializer = PersonViewSerializer(person)
        return Response(serializer.data)