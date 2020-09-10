from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import GetPersonCountWithOrganizationSerializer

from .businesrules import (
    PersonPermissionControl,
    GetAllPersonsWithLen,
    IsManager,
    GetPersonsWithLenManager
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
