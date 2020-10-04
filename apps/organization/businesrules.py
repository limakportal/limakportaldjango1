from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..dashboard.businesrules import GetOrganizationAndLoweOrganization, PersonPermissionControl

from ..person.models import Person
from ..staff.models import Staff
from ..userrole.models import UserRole
from ..organization.models import Organization

from .serializer import OrganizationSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetResponsibleOrganization(request):
    account = request.user
    try:
        person_queryset = Person.objects.get(Email=account.email)
        staff_queryset = Staff.objects.get(Person_id=person_queryset.id)
        organizationArr = []
        if PersonPermissionControl(person_queryset.id, 'ADMIN'):
            organizationArr = list(Organization.objects.all())
        else:
            organizationArr = GetOrganizationAndLoweOrganization(staff_queryset.Organization_id, organizationArr)

            userRole_queryset = UserRole.objects.filter(Account_id=account.id, Organizations__isnull=False)

            for ur in userRole_queryset:
                if len(ur.Organizations) > 0:
                    organizationIdArr = ur.Organizations.split(",")
                    for o in organizationIdArr:
                        organizationArr = GetOrganizationAndLoweOrganization(o, organizationArr)

        organization_serializer_class = OrganizationSerializer(organizationArr, many=True)
    except:
        return Response([])
    return Response(organization_serializer_class.data)
