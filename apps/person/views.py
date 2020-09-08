from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.db import transaction

from .models import Person
from .serializer import PersonSerializer , PersonViewSerializer , PersonViewDetailSerializer , PersonCreateUpdateSerializer
from apps.personidentity.models import PersonIdentity
from apps.personidentity.serializer import PersonIdentitySerializer
from apps.personbusiness.models import PersonBusiness
from apps.personbusiness.serializer import PersonBusinessSerializer
from apps.personeducation.models import PersonEducation
from apps.personeducation.serializer import PersonEducationSerializer
from apps.personfamily.models import PersonFamily
from apps.personfamily.serializer import PersonFamilySerializer
from ..businessrules.views import  HasPermission,GetResponsibleAdminPersonDetails,GetResponsibleIkPersonDetails,GetManagerPersonsDetail,IsManager,GetManagerPersonsDetailNoneSerializer

from ..staff.serializer import StaffSerializer

from ..staff.models import Staff

import io
import json


class PersonViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PersonCreateUpdateSerializer
    queryset = Person.objects.all()


class PersonWithPersonInformationAPIView(APIView):
    def get(self,request):
        if(request.user.is_authenticated):
            p = Person.objects.get(Email = request.user.email)
            if HasPermission(p.id, 'ADMIN'):
                return Response(GetResponsibleAdminPersonDetails(p.id))
            elif HasPermission(p.id, 'IZN_IK'):
                return Response(GetResponsibleIkPersonDetails(p.id))
            elif IsManager(p.id):
                persons = GetManagerPersonsDetailNoneSerializer(p.id)
                serializer = PersonViewSerializer(persons, many=True)
                return Response(serializer.data)
            else:
                persons  =[]
                persons.append(p)
                serializer = PersonViewSerializer(persons, many=True)
                return Response(serializer.data)

        #yetkiye göre gelmeli.
        #persons = Person.objects.all().order_by('id')
        #serializer = PersonViewSerializer(persons,many=True)
        #return Response(serializer.data)

    @transaction.atomic
    def post(self,request):

        transactionSaveId = transaction.savepoint()

        personSerializer = PersonCreateUpdateSerializer(data = request.data['Person'] )
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

            staffSerializer = StaffSerializer(data = request.data['Staff'])
            if len(request.data['Staff']) > 0:
                staffSerializer.initial_data['Person'] = person.id
                if staffSerializer.is_valid():
                    staffSerializer.save()
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
            return Response(data=personSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    def put(self, request, id):

        transactionSaveId = transaction.savepoint()

        person = self.get_object(id)
        getPersonData = {}
        getPersonData = request.data['Person']
        if  request.data['Person']['PictureType'] != None :
            serializer = PersonCreateUpdateSerializer(person, data = getPersonData)
        else:
            serializer = PersonSerializer(person, data = getPersonData)  
        if serializer.is_valid():
            serializer.save()

            getPersonIdentityData = {}
            getPersonIdentityData = request.data['PersonIdentity']
            if len(getPersonIdentityData) > 0:
                if 'id' in json.loads(json.dumps(getPersonIdentityData)):
                    personIdentityObj = PersonIdentity.objects.get(id = getPersonIdentityData['id'])
                    personIdentityEditSerializer = PersonIdentitySerializer(personIdentityObj , data = getPersonIdentityData)
                    if personIdentityEditSerializer.is_valid():
                        personIdentityEditSerializer.save()
                    else:
                        transaction.savepoint_rollback(transactionSaveId)
                        return Response(personIdentityEditSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    personIdentity = PersonIdentity.objects.filter(Person = id)
                    if len(personIdentity) == 0:
                        personIdentityAddSerializer = PersonIdentitySerializer(data = getPersonIdentityData)
                        personIdentityAddSerializer.initial_data['Person'] = id
                        if personIdentityAddSerializer.is_valid():
                            personIdentityAddSerializer.save()
                        else:
                            transaction.savepoint_rollback(transactionSaveId)
                            return Response(personIdentityAddSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

            getPersonBusinessData = {}
            getPersonBusinessData = request.data['PersonBusiness']
            if len(getPersonBusinessData) > 0:
                if 'id' in json.loads(json.dumps(getPersonBusinessData)):
                    personBusinessObj = PersonBusiness.objects.get(id = getPersonBusinessData['id'])
                    personBussinessEddSerializer = PersonBusinessSerializer(personBusinessObj , data = getPersonBusinessData)
                    if personBussinessEddSerializer.is_valid():
                        personBussinessEddSerializer.save()
                    else:
                        transaction.savepoint_rollback(transactionSaveId)
                        return Response(personBussinessEddSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    personBusiness = PersonBusiness.objects.filter(Person = id)
                    if len(personBusiness) == 0:
                        personBusinessAddSerializer = PersonBusinessSerializer(data = getPersonBusinessData)
                        personBusinessAddSerializer.initial_data['Person'] = id
                        if personBusinessAddSerializer.is_valid():
                            personBusinessAddSerializer.save()
                        else:
                            transaction.savepoint_rollback(transactionSaveId)
                            return Response(personBusinessAddSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

            getStaffData = {}
            getStaffData = request.data['Staff']
            if len(getStaffData) > 0:
                if 'id' in json.loads(json.dumps(getStaffData)):
                    staffObj = Staff.objects.get(id = getStaffData['id'])
                    staffEditSerializer = StaffSerializer(staffObj , data = getStaffData)
                    if staffEditSerializer.is_valid():
                        staffEditSerializer.save()
                    else:
                        transaction.savepoint_rollback(transactionSaveId)
                        return Response(staffEditSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    staff = Staff.objects.filter(Person = id)
                    if len(staff) == 0:
                        staffAddSerializer = StaffSerializer(data = getStaffData)
                        staffAddSerializer.initial_data['Person'] = id
                        if staffAddSerializer.is_valid():
                            staffAddSerializer.save()
                        else:
                            transaction.savepoint_rollback(transactionSaveId)
                            return Response(staffAddSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


            getPersonEducationData = {}
            getPersonEducationData = request.data['PersonEducation']
            if len(getPersonEducationData) > 0:
                for educationData in getPersonEducationData:
                    if 'id' in json.loads(json.dumps(educationData)):
                        personEducationObj = PersonEducation.objects.get(id = educationData['id'])
                        personEducationEditSerializer = PersonEducationSerializer(personEducationObj , data = educationData)
                        if personEducationEditSerializer.is_valid():
                            personEducationEditSerializer.save()
                        else:
                            transaction.savepoint_rollback(transaction)
                            return Response(personEducationEditSerializer.errors , status = status.HTTP_400_BAD_REQUEST)
                    else:
                        personEducationAddSerializer = PersonEducationSerializer(data = educationData)
                        personEducationAddSerializer.initial_data['Person'] = id
                        if personEducationAddSerializer.is_valid():
                            personEducationAddSerializer.save()
                        else:
                            transaction.savepoint_rollback(transaction)
                            return Response(personEducationAddSerializer.error_messages , status = status.HTTP_400_BAD_REQUEST)

            getPersonFamiltData = {}
            getPersonFamiltData = request.data['PersonFamily']
            if len(getPersonFamiltData) > 0:
                for familyData in getPersonFamiltData:
                    if 'id' in json.loads(json.dumps(familyData)):
                        personFamilyObj = PersonFamily.objects.get(id = familyData['id'])
                        personFamilyEditSerializer = PersonFamilySerializer(personFamilyObj , data = familyData)
                        if personFamilyEditSerializer.is_valid():
                            personFamilyEditSerializer.save()
                        else:
                            transaction.savepoint_rollback(transaction)
                            return Response(personFamilyEditSerializer.errors , status = status.HTTP_400_BAD_REQUEST)
                    else:
                        personFamilyAddSerializer = PersonFamilySerializer(data = familyData)
                        personFamilyAddSerializer.initial_data['Person'] = id
                        if personFamilyAddSerializer.is_valid():
                            personFamilyAddSerializer.save()
                        else:
                            transaction.savepoint_rollback(transaction)
                            return Response(personFamilyAddSerializer.error_messages , status = status.HTTP_400_BAD_REQUEST)

            


            try:
                newPerson = Person.objects.get(id=id)
                serializer = PersonViewDetailSerializer(newPerson)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND) 

        else:                
            transaction.savepoint_rollback(transactionSaveId)
            