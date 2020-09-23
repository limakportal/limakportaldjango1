from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import GetPersonCountWithOrganizationSerializer, GetAllOrganizationtypeId2WithTotalStaffSerializer
from ..person.serializer import PersonSerializer

from .businesrules import (
    GetOrganizationAndLoweOrganization,
    ListResponsiblePersons
)

from ..organization.models import Organization
from ..staff.models import Staff
from ..person.models import Person
from ..userrole.models import UserRole


@api_view(['GET'])
def GetResponsiblePersons(request, id):
    personArr = ListResponsiblePersons(id)
    result = {}
    result['Persons'] = PersonSerializer(personArr, many=True).data
    if personArr == None:
        result['PersonsLen'] = None
    else:
        result['PersonsLen'] = len(personArr)
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
@permission_classes([IsAuthenticated])
def GetAllOrganizationtypeId2WithTotalStaff(request):
    account = request.user
    try:
        person_queryset = Person.objects.get(Email=account.email)
        staff_queryset = Staff.objects.get(Person_id=person_queryset.id)
        organizationArr = []
        organizationArr = GetOrganizationAndLoweOrganization(staff_queryset.Organization_id, organizationArr)

        userRole_queryset = UserRole.objects.filter(Account_id=account.id, Organizations__isnull=False)

        for ur in userRole_queryset:
            if len(ur.Organizations) > 0:
                organizationIdArr = ur.Organizations.split(",")
                for o in organizationIdArr:
                    organizationArr = GetOrganizationAndLoweOrganization(o, organizationArr)

        organizationType2Arr = []
        for oa in organizationArr:
            if oa.OrganizationType_id == 2:
                organizationType2Arr.append(oa)

        if len(organizationType2Arr) > 0:
            # organization = Organization.objects.filter(OrganizationType_id=2)
            # serializers = GetAllOrganizationtypeId2WithTotalStaffSerializer(organization, many=True)
            serializers = GetAllOrganizationtypeId2WithTotalStaffSerializer(organizationType2Arr, many=True)
            return Response(serializers.data)
    except:
        pass
    return Response([])
