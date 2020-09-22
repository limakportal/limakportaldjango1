from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..dashboard.businesrules import ListResponsiblePersons

from .models import Staff
from ..person.models import Person

from .serializer import StaffJoinSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetResponsibleStaff(request):
    account = request.user
    try:
        person_queryset = Person.objects.get(Email=account.email)
        personArr = ListResponsiblePersons(person_queryset.id)
        staffArr = []
        for p in personArr:
            try:
                staff_queryset = Staff.objects.get(Person_id=p.id)
                staffArr.append(staff_queryset)
            except:
                pass
        serializer = StaffJoinSerializer(staffArr, many=True)
        return Response(serializer.data)
    except:
        return Response([])
