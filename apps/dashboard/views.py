from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import GetPersonCountWithOrganizationSerializer, GetAllOrganizationtypeId2WithTotalStaffSerializer

from .businesrules import (
    PersonPermissionControl,
    GetAllPersonsWithLen,
    IsManager,
    GetPersonsWithLenManager,
    GetOrganizationAndLoweOrganization
)

from ..person.models import Person
from ..organization.models import Organization
from ..staff.models import Staff

from ..person.serializer import PersonSerializer


@api_view(['GET'])
def GetResponsiblePersons(request, id):
    """ Sorumlu Olduğu Personeller """
    if PersonPermissionControl(id, 'ADMIN'):
        return Response(GetAllPersonsWithLen())
    elif PersonPermissionControl(id, 'IZN_IK'):
        return Response(GetAllPersonsWithLen())
    elif IsManager(id):
        return Response(GetPersonsWithLenManager(id))
    else:
        result = {}
        persons = Person.objects.filter(id=id)
        result['Persons'] = PersonSerializer(persons, many=True).data
        result['PersonsLen'] = len(persons)
        return Response(result)


@api_view(['GET'])
def GetPersonCountWithOrganization(request):
    organizationsArr = []
    organizations = Organization.objects.all()
    for o in organizations:
        if len(Staff.objects.filter(Organization_id=o.id)) > 0:
            organizationsArr.append(o)
    serializer = GetPersonCountWithOrganizationSerializer(organizationsArr, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def GetOrganizationResponsiblePersons(request, organizationid):
    organizationsArr = []
    organizations = GetOrganizationAndLoweOrganization(organizationid, organizationsArr)
    serializers = GetPersonCountWithOrganizationSerializer(organizations, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def GetOrganizationWithTotalStaff(request, organizationid):
    result = {}
    try:
        organization = Organization.objects.get(id=organizationid)
        result['organization'] = organization.Name
        organizationsArr = []
        organizations = GetOrganizationAndLoweOrganization(organizationid, organizationsArr)
        totalStaff = 0
        for o in organizations:
            staffs = Staff.objects.filter(Organization_id=o.id)
            totalStaff = totalStaff + len(staffs)
        result['totalstaff'] = str(totalStaff)
    except:
        result['organization'] = None
        result['totalstaff'] = None
    return Response(result)


@api_view(['GET'])
def GetAllOrganizationtypeId2WithTotalStaff(request):
    organization = Organization.objects.filter(OrganizationType_id=2)
    serializers = GetAllOrganizationtypeId2WithTotalStaffSerializer(organization, many=True)
    return Response(serializers.data)
