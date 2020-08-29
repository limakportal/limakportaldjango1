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
from ..permission.models import Permission
from ..authority.models import Authority
from ..userrole.models import UserRole


from ..organization.serializer import OrganizationSerializer ,OrganizationTreeSerializer
from ..businessrules.serializer import (OrganizationTreeByAccountId)
from ..person.serializer import PersonSerializer , PersonViewSerializer



@api_view(['GET'])
def ResponsiblePersonDetails(request, id):
        person = Person.objects.get(id = id)
        account = Account.objects.get(email = person.Email)
        userRoles = UserRole.objects.filter(Account_id = account.id)
        for userRole in userRoles:
            try:
                authorityes = Authority.objects.filter(Role_id = userRole.Role_id)
                if len(authorityes) > 0:
                    for authority in authorityes:
                        permissions = Permission.objects.filter(Code = code)
                        for permission in permissions:
                            if permission.id == authority.Permission_id:
                                response = {}
                                response['ResponsiblePersons'] = GetResponsibleIkPersonDetails(id)
                                return Response(response,status=status.HTTP_200_OK)
            except:
                return False


def GetResponsibleIkPersonDetails(id):
    persons = Person.objects.all()
    serializer = PersonViewSerializer(persons , many = True)
    return serializer.data

def GetResponsibleIkPersons():
    ikPersons = []
    permissions = Permission.objects.filter(Code = 'IZN_IK')
    for permission in permissions:
        authorityes = Authority.objects.filter(Permission = permission.id)
        for authority in authorityes:
            userRoles = UserRole.objects.filter(Role = authority.Role_id)
            for userRole in userRoles:
                try:
                    account = Account.objects.get(id = userRole.Account_id)
                    person = Person.objects.get(Email = account.email)
                    ikPersons.append(person)
                except :
                    pass

    return PersonSerializer(ikPersons , many = True).data


def GetResponsiblePersonDetails(id):
    try:
            person = Person.objects.get(id = id)
            staff = Staff.objects.get(Person = person.id)

            organizationObj = Organization.objects.get(id = staff.Organization_id)
            serializer = OrganizationWithPersonTreeSerializer(organizationObj)
            responsibleMenu = serializer.data

            personRequest = {}

            try:
                personRequest = PersonViewSerializer(person).data

            except :
                personRequest = None

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

            responsiblePersons = PersonViewSerializer(persons ,many=True).data
    except :
            return None , None, None
    return responsibleMenu,responsiblePersons,personRequest

def GetResponsibleIkPersons():
    ikPersons = []
    permissions = Permission.objects.filter(Code = 'IZN_IK')
    for permission in permissions:
        authorityes = Authority.objects.filter(Permission = permission.id)
        for authority in authorityes:
            userRoles = UserRole.objects.filter(Role = authority.Role_id)
            for userRole in userRoles:
                try:
                    account = Account.objects.get(id = userRole.Account_id)
                    person = Person.objects.get(Email = account.email)
                    ikPersons.append(person)
                except :
                    pass

    return PersonSerializer(ikPersons , many = True).data

@api_view(['GET'])
def AccountListDetails(request):
    accounts = Account.objects.all()
    serializers = AccountsDetailSerializer(accounts , many = True)
    return Response(serializers.data)

def mail_yolla(baslik,icerik,to,send):
    # baslik = 'İzin Kullanım Hakkında'
    # icerik = 'Ayça Bilmez’in ... tarihine kadar ... gün iznini kullanması gerekmektedir. Lütfen çalışanınızı mevcut iznini kullanmaya yönlendiriniz.'
    send_mail(baslik, icerik, to, send, fail_silently=False)