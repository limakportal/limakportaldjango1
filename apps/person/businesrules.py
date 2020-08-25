from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
import json

from ..staff.models import Staff
from ..organization.models import Organization
from .models import Person
from .serializer import PersonSerializer
from .serializer import PersonViewSerializer
from ..personidentity.models import PersonIdentity
from .serializer import PersonIdentitySerializer
from rest_framework.decorators import api_view
from datetime import datetime

@api_view(['GET'])
def PersonApprover(request, id):
        try:
            staff = Staff.objects.get(Person = id)
            organization = Organization.objects.get(id = staff.Organization.id)
            if organization.CanApproveRight:
                if organization.ManagerTitle == None:
                    return Response('Kişinin bağlı olduğu birimde yönetici bulunmamaktadır.',status=status.HTTP_404_NOT_FOUND)
                
                ystaff = Staff.objects.get(Organization=organization.id,Title = organization.ManagerTitle.id)
                
                if ystaff == None:
                    return Response('Kişinin bağlı olduğu birimde yönetici bulunmamaktadır.',status=status.HTTP_404_NOT_FOUND)
                personel = Person.objects.get(id=ystaff.Person.id)
                if personel.id == id:
                    staffs = Staff.objects.get(Organization = organization.UpperOrganization.id)
                    personel = Person.objects.get(id=staffs.Person.id)
                    serializer = PersonSerializer(personel)
                    data = {}
                    data['id'] = serializer.data['id']
                    data['FullName'] = serializer.data['Name'] + ' ' + serializer.data['Surname']
                    return Response(data)
                serializer = PersonSerializer(personel)
                data = {}
                data['id'] = serializer.data['id']
                data['FullName'] = serializer.data['Name'] + ' ' + serializer.data['Surname']
                return Response(data)
            else:
                neworganization = Organization.objects.get(id = organization.UpperOrganization.id)
                if neworganization.CanApproveRight:
                    newstaff = Staff.objects.get(Organization=neworganization.id,Title = neworganization.ManagerTitle.id)
                
                if newstaff == None:
                    return Response('Kişinin bağlı olduğum birimde yönetici bulunmamaktadır.',status=status.HTTP_404_NOT_FOUND)
                personel = Person.objects.get(id=newstaff.Person.id)
                if personel.id == id:
                    staffs = Staff.objects.get(Organization = organization.UpperOrganization.id)
                    personel = Person.objects.get(id=staffs.Person.id)
                    serializer = PersonSerializer(personel)
                    data = {}
                    data['id'] = serializer.data['id']
                    data['FullName'] = serializer.data['Name'] + ' ' + serializer.data['Surname']
                    return Response(data)
                serializer = PersonSerializer(personel)
                data = {}
                data['id'] = serializer.data['id']
                data['FullName'] = serializer.data['Name'] + ' ' + serializer.data['Surname']
                return Response(data)
                # staffs = Staff.objects.get(Organization = organization.UpperOrganization.id)
                # personel = Person.objects.get(id=staffs.Person.id)
                # serializer = PersonSerializer(personel)
                # data = {}
                # data['id'] = serializer.data['id']
                # data['FullName'] = serializer.data['Name'] + ' ' + serializer.data['Surname']
                # return Response(data)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

def GetPersonApprover(id):
        staff = Staff.objects.get(Person = id)
        organization = Organization.objects.get(id = staff.Organization.id)
        if organization.CanApproveRight:
            personel = Person.objects.get(id=id)
            serializer = PersonSerializer(personel)
        else:
            staffs = Staff.objects.get(Organization = organization.UpperOrganization.id)
            personel = Person.objects.get(id=staffs.Person.id)
            serializer = PersonSerializer(personel)
        
        return serializer

@api_view(['GET'])
def bornTodayPerson(request):
    try:
        today = datetime.now()
        day = today.day
        month = today.month    
        
        personidentities = PersonIdentity.objects.filter(BirthDate__day = day, BirthDate__month = month)
        persons = []
        for personIdenty in personidentities:
            person = Person.objects.get(id = personIdenty.Person_id)
            staff = Staff.objects.get(id = personIdenty.Person_id)
            persons.append(person)
            persons.append(staff)
        serializer = PersonViewSerializer(persons,many=True)
        return Response(serializer.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def bornMonthPerson(request):
    try:
        today = datetime.now()
        month = today.month    
        
        personidentities = PersonIdentity.objects.filter(BirthDate__month = month)
        persons = []
        for personIdenty in personidentities:
            person = Person.objects.get(id = personIdenty.Person_id)
            staff = Staff.objects.get(id = personIdenty.Person_id)
            persons.append(person)
            persons.append(staff)
        serializer = PersonViewSerializer(persons,many=True)
        return Response(serializer.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)