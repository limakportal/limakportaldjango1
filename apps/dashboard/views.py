from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .businesrules import(
    PersonPermissionControl, 
    GetAllPersonsWithLen,
    IsManager,
    GetPersonsWithLenManager
    )

from ..person.models import Person
from ..staff.models import Staff
from ..organization.models import Organization

from ..person.serializer import PersonSerializer

@api_view(['GET'])
def GetResponsiblePersons(request,id):
        if PersonPermissionControl(id,'ADMIN'):                       
            return Response(GetAllPersonsWithLen())
        elif PersonPermissionControl(id,'IZN_IK'):
            return Response(GetAllPersonsWithLen())
        elif IsManager(id):
            return Response(GetPersonsWithLenManager(id))
        else:
            result = {}
            persons = Person.objects.filter(id = id)
            result['Persons'] = PersonSerializer(persons , many = True).data
            result['PersonsLen'] = len(persons)
            return Response(result)
