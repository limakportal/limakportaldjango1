from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.core.mail import send_mail

from .serializer import OrganizationWithPersonTreeSerializer, AccountsDetailSerializer

from ..organization.models import Organization
from ..staff.models import Staff
from ..person.models import Person
from ..account.models import Account
from ..permission.models import Permission
from ..authority.models import Authority
from ..userrole.models import UserRole

from ..person.serializer import PersonSerializer, PersonViewSerializer
from ..dashboard.businesrules import ListResponsiblePersons


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ResponsiblePersonDetails(request, id):
    response = {}

    response['ResponsibleMenu'], response['ResponsiblePersons'], response['Person'] = GetResponsiblePersonDetails(id)

    return Response(response, status=status.HTTP_200_OK)


def GetPersonsByOrganizationId(organizationId, personArr):
    try:
        # bu birimdeki kadrolar ve personeller
        allStaff = Staff.objects.filter(Organization_id=organizationId)
        for s in allStaff:
            try:
                person = Person.objects.get(id=s.Person_id)
                personArr.append(person)
            except:
                pass

        altBirimler = Organization.objects.filter(UpperOrganization=organizationId)

        for o in altBirimler:
            GetPersonsByOrganizationId(o.id, personArr)
        return personArr
    except:
        return None


def GetOrganizationByID(organizationId, organizationArr):
    try:
        try:
            organization = Organization.objects.get(id=organizationId)
            organizationArr.append(organization)
        except:
            pass
        altBirimler = Organization.objects.filter(UpperOrganization=organizationId)
        for o in altBirimler:
            GetOrganizationByID(o.id, organizationArr)
        return organizationArr
    except:
        return None


def GetManagerPersonsDetailNoneSerializer(personId):
    try:
        staff = Staff.objects.get(Person_id=personId)
        personArr = []
        return GetPersonsByOrganizationId(staff.Organization_id, personArr)
    except:
        return None


def GetManagerOrganizationsDetailNoneSerializer(personId):
    try:
        staff = Staff.objects.get(Person_id=personId)
        organizationArr = []
        return GetOrganizationByID(staff.Organization_id, organizationArr)
    except:
        return None


def GetManagerPersonsDetail(personId):
    try:
        staff = Staff.objects.get(Person_id=personId)
        personArr = []

        persons = GetPersonsByOrganizationId(staff.Organization_id, personArr)
        return PersonSerializer(persons, many=True).data

    except:
        return None


def HasPermission(id, code):
    try:
        person = Person.objects.get(id=id)
        account = Account.objects.get(email=person.Email)
        userRoles = UserRole.objects.filter(Account_id=account.id)
        for userRole in userRoles:
            authorityes = Authority.objects.filter(Role_id=userRole.Role_id)
            if len(authorityes) > 0:
                for authority in authorityes:
                    permissions = Permission.objects.filter(Code=code)
                    for permission in permissions:
                        if permission.id == authority.Permission_id:
                            return True
    except:
        return False


def GetResponsibleIkPersonDetails(id):
    try:
        person = Person.objects.get(id=id)
        staff = Staff.objects.get(Person_id=person.id)

        organizationObj = Organization.objects.get(id=staff.Organization_id)
        serializer = OrganizationWithPersonTreeSerializer(organizationObj)
        responsibleMenu = serializer.data

        persons = []

        sameStaffs = Staff.objects.filter(Organization=staff.Organization_id)
        for staff in sameStaffs:
            try:
                person = Person.objects.get(id=staff.Person_id)
                persons.append(person)
            except:
                person = None

        if responsibleMenu['ChildOrganization'] != None:
            for child in responsibleMenu['ChildOrganization']:
                staffs = Staff.objects.filter(Organization=child['id'])
                for staff in staffs:
                    try:
                        person = Person.objects.get(id=staff.Person_id)
                        persons.append(person)
                    except:
                        person = None

        return PersonViewSerializer(persons, many=True).data
    except:
        return None


def GetResponsibleAdminPersonDetails(id):
    persons = Person.objects.all().order_by("Name")
    serializer = PersonViewSerializer(persons, many=True)
    return serializer.data


def GetResponsibleIkPersons():
    ikPersons = []
    permissions = Permission.objects.filter(Code='IZN_IK')
    for permission in permissions:
        authorityes = Authority.objects.filter(Permission=permission.id)
        for authority in authorityes:
            userRoles = UserRole.objects.filter(Role=authority.Role_id)
            for userRole in userRoles:
                try:
                    account = Account.objects.get(id=userRole.Account_id)
                    person = Person.objects.get(Email=account.email)
                    ikPersons.append(person)
                except:
                    pass

    return PersonSerializer(ikPersons, many=True).data


def GetResponsiblePersonDetails(id):
    try:
        person = Person.objects.get(id=id)
        staff = Staff.objects.get(Person=person.id)

        organizationObj = Organization.objects.get(id=staff.Organization_id)
        serializer = OrganizationWithPersonTreeSerializer(organizationObj)
        responsibleMenu = serializer.data

        personRequest = {}

        try:
            personRequest = PersonViewSerializer(person).data

        except:
            personRequest = None

        persons = []
        if responsibleMenu['ChildOrganization'] != None:
            for child in responsibleMenu['ChildOrganization']:
                staffs = Staff.objects.filter(Organization=child['id'])
                for staff in staffs:
                    try:
                        person = Person.objects.get(id=staff.Person_id)
                        persons.append(person)
                    except:
                        person = None

        try:
            personArr = ListResponsiblePersons(id)
            responsiblePersons = PersonViewSerializer(personArr, many=True).data
        except:
            responsiblePersons = None




    except:
        return None, None, None
    return responsibleMenu, responsiblePersons, personRequest


def GetResponsibleIkPersons():
    ikPersons = []
    permissions = Permission.objects.filter(Code='IZN_IK')
    for permission in permissions:
        authorityes = Authority.objects.filter(Permission=permission.id)
        for authority in authorityes:
            userRoles = UserRole.objects.filter(Role=authority.Role_id)
            for userRole in userRoles:
                try:
                    account = Account.objects.get(id=userRole.Account_id)
                    person = Person.objects.get(Email=account.email)
                    ikPersons.append(person)
                except:
                    pass

    return PersonSerializer(ikPersons, many=True).data


def IsManager(personId):
    try:
        staff = Staff.objects.get(Person_id=personId)
        organization = Organization.objects.get(id=staff.Organization_id)
        if organization.ManagerTitle_id == staff.Title_id and staff.Organization_id == organization.id:
            return True
        return False
    except:
        return False


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ManagerPersons(request):
    account = request.user
    try:
        person_queryset = Person.objects.get(Email=account.email)

        personArr = []
        staff_queryset = Staff.objects.get(Person_id=person_queryset.id)
        staffs_queryset = Staff.objects.filter(Organization_id=staff_queryset.Organization)
        for s in staffs_queryset:
            try:
                person_queryset = Person.objects.get(id=s.Person_id)
                personArr.append(person_queryset)
            except:
                pass

        userRole_queryset = UserRole.objects.filter(Account_id=account.id, Organizations__isnull=False)
        if len(userRole_queryset) > 0:
            for ur in userRole_queryset:
                if len(ur.Organizations) > 0:
                    organizationIdArr = ur.Organizations.split(",")
                    for o in organizationIdArr:
                        staffs_queryset = Staff.objects.filter(Organization_id=o)
                        for s in staffs_queryset:
                            try:
                                person_queryset = Person.objects.get(id=s.Person_id)
                                personArr.append(person_queryset)
                            except:
                                pass

        managerpersons = []
        # persons = Person.objects.all()
        # for person in persons:
        #     if IsManager(person.id):
        #         managerpersons.append(person)
        # return Response(PersonSerializer(managerpersons, many=True).data)

        for person in personArr:
            if IsManager(person.id):
                managerpersons.append(person)
        return Response(PersonSerializer(managerpersons, many=True).data)

    except:
        Response([])


@api_view(['GET'])
def AccountListDetails(request):
    accounts = Account.objects.all()
    serializers = AccountsDetailSerializer(accounts, many=True)
    return Response(serializers.data)


def mail_yolla(baslik, icerik, to, send):
    # baslik = 'İzin Kullanım Hakkında'
    # icerik = 'Ayça Bilmez’in ... tarihine kadar ... gün iznini kullanması gerekmektedir. Lütfen çalışanınızı mevcut iznini kullanmaya yönlendiriniz.'
    send_mail(baslik, icerik, to, send, fail_silently=False)
