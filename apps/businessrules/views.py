from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.core.mail import send_mail

from ..organization.models import Organization
from ..staff.models import Staff
from ..person.models import Person
from ..account.models import Account
from ..permission.models import Permission
from ..authority.models import Authority
from ..userrole.models import UserRole

from .serializer import OrganizationWithPersonTreeSerializer, AccountsDetailSerializer
from ..person.serializer import PersonSerializer, PersonViewSerializer

from ..dashboard.businesrules import ListResponsiblePersons, IsManager


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
            if len(personArr) > 1:
                personArr.sort(key=lambda x:x.Name.lower())
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ManagerPersons(request):
    manager_Arr = []
    account = request.user
    try:
        person_queryset = Person.objects.get(Email=account.email)
        staff_queryset = Staff.objects.get(Person_id=person_queryset.id)
        if IsManager(person_queryset.id):
            try:
                organization_queryset = Organization.objects.get(id=staff_queryset.Organization_id)
                upper_organization_queryset = Organization.objects.filter(id=organization_queryset.UpperOrganization_id)
                for o in upper_organization_queryset:
                    staff_in_organization_queryset = Staff.objects.filter(Organization_id=o.id)
                    for s in staff_in_organization_queryset:
                        if IsManager(s.Person_id):
                            try:
                                manager_queryset = Person.objects.get(id=s.Person_id)
                                manager_Arr.append(manager_queryset)
                            except:
                                pass
            except:
                pass
        else:
            staff_in_organization_queryset = Staff.objects.filter(Organization_id=staff_queryset.Organization_id)
            for s in staff_in_organization_queryset:
                if IsManager(s.Person_id):
                    try:
                        manager_queryset = Person.objects.get(id=s.Person_id)
                        manager_Arr.append(manager_queryset)
                    except:
                        pass

        userRole_queryset = UserRole.objects.filter(Account_id=account.id, Organizations__isnull=False)
        if len(userRole_queryset) > 0:
            for ur in userRole_queryset:
                if len(ur.Organizations) > 0:
                    organizationIdArr = ur.Organizations.split(",")
                    for o in organizationIdArr:
                        staff_in_organization_queryset = Staff.objects.filter(Organization_id=o)
                        for s in staff_in_organization_queryset:
                            if IsManager(s.Person_id):
                                try:
                                    manager_queryset = Person.objects.get(id=s.Person_id)
                                    if manager_queryset not in manager_Arr: ## Bu person array de yok ise ekleme yapıyor
                                        manager_Arr.append(manager_queryset)
                                except:
                                    pass



    except:
        pass
    return Response(PersonSerializer(manager_Arr, many=True).data)


@api_view(['GET'])
def AccountListDetails(request):
    accounts = Account.objects.all()
    serializers = AccountsDetailSerializer(accounts, many=True)
    return Response(serializers.data)


def mail_yolla(baslik, icerik, to, send):
    # baslik = 'İzin Kullanım Hakkında'
    # icerik = 'Ayça Bilmez’in ... tarihine kadar ... gün iznini kullanması gerekmektedir. Lütfen çalışanınızı mevcut iznini kullanmaya yönlendiriniz.'
    send_mail(baslik, icerik, to, send, fail_silently=False)
