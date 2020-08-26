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

        try:

            account = Account.objects.get(id = id)
            person = Person.objects.get(Email = account.email)
            staff = Staff.objects.get(Person = person.id)



            organizationObj = Organization.objects.get(id = staff.Organization_id)
            serializer = OrganizationWithPersonTreeSerializer(organizationObj)
            response['ResponsibleMenu'] = serializer.data

            persons = []
            # staffs = Staff.objects.filter(Organization = response['ResponsibleMenu']['id'])
            # for staff in staffs:
            #     try:
            #         person = Person.objects.get(id = staff.Person_id)
            #         persons.append(person)
            #     except:
            #         person = None
            if response['ResponsibleMenu']['ChildOrganization'] != None:
                for child in response['ResponsibleMenu']['ChildOrganization']:
                    staffs = Staff.objects.filter(Organization = child['id'])
                    for staff in staffs:
                        try:
                            person = Person.objects.get(id = staff.Person_id)
                            persons.append(person)
                        except:
                            person = None

            response['ResponsiblePersons'] = PersonSerializer(persons ,many=True).data
        except :
            response['ResponsibleMenu'] = None
            response['ResponsiblePersons'] = None

        return Response(response,status=status.HTTP_200_OK)

@api_view(['GET'])
def AccountListDetails(request):
    accounts = Account.objects.all()
    serializers = AccountsDetailSerializer(accounts , many = True)
    return Response(serializers.data)

def mail_yolla(baslik,icerik,to,send):
    # baslik = 'İzin Kullanım Hakkında'
    # icerik = 'Ayça Bilmez’in ... tarihine kadar ... gün iznini kullanması gerekmektedir. Lütfen çalışanınızı mevcut iznini kullanmaya yönlendiriniz.'
    send_mail(baslik, icerik, to, send, fail_silently=False)