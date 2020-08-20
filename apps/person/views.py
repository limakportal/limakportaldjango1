from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from .models import Person
from .serializer import PersonSerializer , PersonViewSerializer , PersonViewDetailSerializer
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

        personSerializer = PersonSerializer(data = request.data['Person'] )
        if personSerializer.is_valid():
            person = personSerializer.save()

            personIdentitySerializer = PersonIdentitySerializer(data = request.data['PersonIdentity'])   
            if len(request.data['PersonIdentity']) > 0 :
                personIdentitySerializer.initial_data['Person'] = person.id               
                if personIdentitySerializer.is_valid():
                    personIdentitySerializer.save()
                else:
                    transaction.savepoint_rollback(transactionSaveId)

            personbusinessSerializer = PersonBusinessSerializer(data = request.data['PersonBusiness'])
           
            if len(request.data['PersonBusiness']) > 0:
                personbusinessSerializer.initial_data['Person'] = person.id 
                if personbusinessSerializer.is_valid():
                    personbusinessSerializer.save()
                else:
                    transaction.savepoint_rollback(transactionSaveId)


            if len(request.data['PersonEducation']) > 0:
                for personEducation in request.data['PersonEducation']:
                    personEducationSerializer = PersonEducationSerializer(data=personEducation)
                    personEducationSerializer.initial_data['Person'] = person.id
                    if personEducationSerializer.is_valid():
                        personEducationSerializer.save()
                    else:
                        transaction.savepoint_rollback(transactionSaveId)

            if len(request.data['PersonFamily']) > 0:
                for personFamily in request.data['PersonFamily']:
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
        serializer = PersonViewDetailSerializer(person)
        return Response(serializer.data)

    @transaction.atomic
    def put(self, request,id):
        print('emrah')

        transactionSaveId = transaction.savepoint()

        person = self.get_object(id)
        serializer = PersonSerializer(person, data=request.data['Person'])
        if serializer.is_valid():
            serializer.save()
            
            if len(request.data['PersonIdentity']) > 0:
                try:
                    personIdentity = PersonIdentity.objects.get(id = request.data['PersonIdentity']['id'])
                    personIdentitySerializer = PersonIdentitySerializer(personIdentity , data = request.data['PersonIdentity'])
                    if personIdentitySerializer.is_valid():
                        personIdentitySerializer.save()
                    else:
                        transaction.savepoint_rollback(transactionSaveId)
                        return Response(personIdentitySerializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except PersonIdentity.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)

            if len(request.data['PersonBusiness']) > 0:
                try:
                    personBusiness = PersonBusiness.objects.get(id = request.data['PersonBusiness']['id'])
                    personBusinessSerializer = PersonBusinessSerializer(personBusiness , data = request.data['PersonBusiness'])
                    if personBusinessSerializer.is_valid():
                        personBusinessSerializer.save()
                    else:
                        transaction.savepoint_rollback(transaction)
                        return Response(personBusinessSerializer.errors , status = status.HTTP_400_BAD_REQUEST)
                except PersonIdentity.DoesNotExist:
                    return Response(status = status.HTTP_404_NOT_FOUND)

            if len(request.data['PersonEducation']) > 0:
                for peronEducationData in request.data['PersonEducation']:
                    try:
                        personEducation = PersonEducation.objects.get(id = peronEducationData['id'])
                        personEducationSerializer = PersonEducationSerializer(personEducation , data = peronEducationData)
                        if personEducationSerializer.is_valid():
                            personEducationSerializer.save()
                        else:
                            transaction.savepoint_rollback(transaction)
                            return Response(personEducationSerializer.errors , status = status.HTTP_400_BAD_REQUEST)
                    except PersonEducation.DoesNotExist:
                        return Response(status = status.HTTP_404_NOT_FOUND)

            if len(request.data['PersonFamily']) > 0:
                for personFamilyData in request.data['PersonFamily']:
                    try:
                        personFamily = PersonFamily.objects.get(id = personFamilyData['id'])
                        personFamilySerializer = PersonEducationSerializer(personFamily , data = personFamilyData)
                        if personFamilySerializer.is_valid():
                            personFamilySerializer.save()
                        else:
                            transaction.savepoint_rollback(transaction)
                            return Response(personFamilySerializer.errors , status = status.HTTP_400_BAD_REQUEST)
                    except expression as identifier:
                        return Response(status = status.HTTP_404_NOT_FOUND)

            try:
                newPerson = Person.objects.get(id=id)
                serializer = PersonViewSerializer(newPerson)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND) 

        else:                
            transaction.savepoint_rollback(transactionSaveId)
            