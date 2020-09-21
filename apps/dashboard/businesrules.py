from ..person.models import Person
from ..account.models import Account
from ..userrole.models import UserRole
from ..authority.models import Authority
from ..permission.models import Permission
from ..staff.models import Staff
from ..organization.models import Organization

from ..person.serializer import PersonSerializer


def PersonPermissionControl(personId, permissionCode):
    """ ADMIN ve IZN_IK Yetki Kontrol """
    try:
        person = Person.objects.get(id=personId)
        account = Account.objects.get(email=person.Email)
        userRoles = UserRole.objects.filter(Account_id=account.id)
        for userRole in userRoles:
            authorityes = Authority.objects.filter(Role_id=userRole.Role_id)
            if len(authorityes) > 0:
                for authority in authorityes:
                    permissions = Permission.objects.filter(Code=permissionCode)
                    for permission in permissions:
                        if permission.id == authority.Permission_id:
                            return True
    except:
        return False


def GetAllIkResponsiblePersonWithLen(personId):
    result = {}
    try:
        account = Account.objects.get(email=Person.objects.get(id=personId))
        userrole = UserRole.objects.get(Account_id=account.id)
        organizationIdArr = userrole.Organizations.split(",")
        personArr = []
        for o in organizationIdArr:
            personsArr = []
            persons = GetPersonsByOrganizationId(o, personsArr)
            for p in persons:
                personArr.append(p)
        result['Persons'] = PersonSerializer(personArr, many=True).data
        result['PersonsLen'] = len(personArr)

    except:
        result['Persons'] = None
        result['PersonsLen'] = None


def GetAllPersonsWithLen():
    """ Bütün Personeller ve Sayısı """
    result = {}
    persons = Person.objects.all()
    result['Persons'] = PersonSerializer(persons, many=True).data
    result['PersonsLen'] = len(persons)
    return result


def IsManager(personId):
    """ Personel Yönetici Kontrol """
    try:
        staff = Staff.objects.get(Person_id=personId)
        organization = Organization.objects.get(id=staff.Organization_id)
        if organization.ManagerTitle_id == staff.Title_id and staff.Organization_id == organization.id:
            return True
        return False
    except:
        return False


def GetPersonsWithLenManager(personId):
    """ Yöneticinin Sorumlu Olduğu Personeller ve Sayısı """
    result = {}
    staff = Staff.objects.get(Person_id=personId)
    personsArr = []
    persons = GetPersonsByOrganizationId(staff.Organization_id, personsArr)
    result['Persons'] = PersonSerializer(persons, many=True).data
    result['PersonsLen'] = len(persons)
    return result


def GetPersonsByOrganizationId(organizationId, personArr):
    """ Yöneticinin Sorumlu Olduğu Personeller ve Sayısı """
    try:
        staffs = Staff.objects.filter(Organization_id=organizationId)
        for s in staffs:
            try:
                person = Person.objects.get(id=s.Person_id)
                personArr.append(person)
            except:
                pass

        lowerOrganization = Organization.objects.filter(UpperOrganization=organizationId)

        for o in lowerOrganization:
            GetPersonsByOrganizationId(o.id, personArr)
        return personArr
    except:
        return None


def GetOrganizationAndLoweOrganization(organizationId, organizationArr):
    """Organzation and lowerOrganization"""
    try:
        organization = Organization.objects.get(id=organizationId)
        organizationArr.append(organization)
    except:
        pass
    lowerOrganization = Organization.objects.filter(UpperOrganization=organizationId)
    for o in lowerOrganization:
        GetOrganizationAndLoweOrganization(o.id, organizationArr)
    return organizationArr
