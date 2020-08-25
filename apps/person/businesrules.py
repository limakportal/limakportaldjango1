from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
import json

from ..staff.models import Staff
from ..organization.models import Organization
from .models import Person
from .serializer import PersonSerializer


class PersonApproverDetails(APIView):

    def get(self, request, id):
        try:
            staff = Staff.objects.get(Person = id)
            organization = Organization.objects.get(id = staff.Organization.id)
            if organization.CanApproveRight:
                ystaff = Staff.objects.get(Organization=organization.id,Title = organization.ManagerTitle.id)
                
                if ystaff == None:
                    return Response('Kişinin bağlı olduğum birimde yönetici bulunmamaktadır.',status=status.HTTP_404_NOT_FOUND)
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
                staffs = Staff.objects.get(Organization = organization.UpperOrganization.id)
                personel = Person.objects.get(id=staffs.Person.id)
                serializer = PersonSerializer(personel)
                data = {}
                data['id'] = serializer.data['id']
                data['FullName'] = serializer.data['Name'] + ' ' + serializer.data['Surname']
                return Response(data)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)