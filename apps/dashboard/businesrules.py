from ..person.models import Person
from ..account.models import Account
from ..userrole.models import UserRole
from ..authority.models import Authority
from ..permission.models import Permission
from ..staff.models import Staff
from ..organization.models import Organization


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
    try:
        account = Account.objects.get(email=Person.objects.get(id=personId).Email)
        userrole = UserRole.objects.filter(Account_id=account.id, Organizations__isnull=False)
        personArr = []
        if len(userrole) > 0:
            for u in userrole:
                if len(u.Organizations) > 0:
                    organizationIdArr = u.Organizations.split(",")
                    for o in organizationIdArr:
                        if len(o) > 0:
                            personsArr = []
                            persons = GetPersonsByOrganizationId(o, personsArr)
                            for p in persons:
                                personArr.append(p)
    except:
        personArr = []

    return personArr


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
    person_Arr = []

    try:
        staff_queryset = Staff.objects.get(Person_id=personId)
        person_Arr = GetPersonsByOrganizationId(staff_queryset.Organization_id, person_Arr)

        try:
            account_queryset = Account.objects.get(email=Person.objects.get(id=personId).Email)
            userRole_queryset = UserRole.objects.filter(Account_id=account_queryset.id, Organizations__isnull=False)
            if len(userRole_queryset) > 0:
                for ur in userRole_queryset:
                    if len(ur.Organizations) > 0:
                        organizationIdArr = ur.Organizations.split(",")
                        for o in organizationIdArr:
                            staffs_queryset = Staff.objects.filter(Organization_id=o)
                            for s in staffs_queryset:
                                try:
                                    person_queryset = Person.objects.get(id=s.Person_id)
                                    if person_queryset in person_Arr:
                                        break
                                    person_Arr.append(person_queryset)
                                except:
                                    pass

        except:
            pass

    except:
        pass

    return person_Arr


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


def ListResponsiblePersons(personid):
    """ Sorumlu Olduğu Personeller """
    if PersonPermissionControl(personid, 'ADMIN'):
        return Person.objects.all()
    elif PersonPermissionControl(personid, 'IZN_IK'):
        return GetAllIkResponsiblePersonWithLen(personid)
    elif IsManager(personid):
        return GetPersonsWithLenManager(personid)
    else:
        persons = Person.objects.filter(id=personid)
        return persons
