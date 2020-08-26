from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from django.core.mail import send_mail
import json

from .serializer import OrganizationWithPersonTreeSerializer , AccountsDetailSerializer

from ..organization.models import Organization
from ..staff.models import Staff
from ..person.models import Person
from ..account.models import Account


from ..organization.serializer import OrganizationSerializer ,OrganizationTreeSerializer
from ..businessrules.serializer import (OrganizationTreeByAccountId)
from ..person.serializer import PersonSerializer



@api_view(['GET'])
def ResponsiblePersonDetails(request, id):
        response = {}
        response['ResponsibleMenu'],response['ResponsiblePersons'] = GetResponsiblePersonDetails(id)

        return Response(response,status=status.HTTP_200_OK)

def GetResponsiblePersonDetails(id):
    try:
            person = Person.objects.get(id = id)
            staff = Staff.objects.get(Person = person.id)

            organizationObj = Organization.objects.get(id = staff.Organization_id)
            serializer = OrganizationWithPersonTreeSerializer(organizationObj)
            responsibleMenu = serializer.data

            persons = []
            if responsibleMenu['ChildOrganization'] != None:
                for child in responsibleMenu['ChildOrganization']:
                    staffs = Staff.objects.filter(Organization = child['id'])
                    for staff in staffs:
                        try:
                            person = Person.objects.get(id = staff.Person_id)
                            persons.append(person)
                        except:
                            person = None

            responsiblePersons = PersonSerializer(persons ,many=True).data
    except :
            responsibleMenu = None
            ResponsiblePersons= None
    return responsibleMenu,responsiblePersons

@api_view(['GET'])
def AccountListDetails(request):
    accounts = Account.objects.all()
    serializers = AccountsDetailSerializer(accounts , many = True)
    return Response(serializers.data)

def mail_yolla(baslik,icerik,to,send):
    # baslik = 'İzin Kullanım Hakkında'
    # icerik = 'Ayça Bilmez’in ... tarihine kadar ... gün iznini kullanması gerekmektedir. Lütfen çalışanınızı mevcut iznini kullanmaya yönlendiriniz.'
    send_mail(baslik, icerik, to, send, fail_silently=False)