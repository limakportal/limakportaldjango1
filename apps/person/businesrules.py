from rest_framework.response import Response
from rest_framework import status

from ..staff.models import Staff
from ..organization.models import Organization
from .models import Person
from .serializer import PersonSerializer
from ..personidentity.models import PersonIdentity
from rest_framework.decorators import api_view
from datetime import datetime
from ..title.models import Title
from datetime import datetime

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Person
from .serializer import PersonSerializer
from ..organization.models import Organization
from ..personidentity.models import PersonIdentity
from ..staff.models import Staff
from ..title.models import Title


@api_view(['GET'])
def PersonApprover(request, id):
    global newstaff
    try:
        staff = Staff.objects.get(Person=id)
        organization = Organization.objects.get(id=staff.Organization.id)
        if organization.CanApproveRight:
            if organization.ManagerTitle is None:
                return Response('Kişinin bağlı olduğu birimde yönetici bulunmamaktadır.',
                                status=status.HTTP_404_NOT_FOUND)

            ystaff = Staff.objects.get(Organization=organization.id, Title=organization.ManagerTitle.id)

            if ystaff is None:
                return Response('Kişinin bağlı olduğu birimde yönetici bulunmamaktadır.',
                                status=status.HTTP_404_NOT_FOUND)
            personel = Person.objects.get(id=ystaff.Person.id)
            if personel.id == id:
                staffs = Staff.objects.filter(Organization=organization.UpperOrganization.id)
                if len(staffs) == 0:
                    return Response('Kişinin bağlı olduğu birimde yönetici bulunmamaktadır.',
                                    status=status.HTTP_404_NOT_FOUND)
                personel = Person.objects.get(id=staffs[0].Person.id)
                serializer = PersonSerializer(personel)
                data = {}
                data['id'] = serializer.data['id']
                data['FullName'] = serializer.data['Name'] + ' ' + serializer.data['Surname']
                return Response(data)
            serializer = PersonSerializer(personel)
            data = {}
            data['id'] = serializer.data['id']
            data['FullName'] = serializer.data['Name'] + ' ' + serializer.data['Surname']
            return Response(data)
        else:
            neworganization = Organization.objects.get(id=organization.UpperOrganization.id)
            if neworganization.CanApproveRight:
                newstaff = Staff.objects.get(Organization=neworganization.id, Title=neworganization.ManagerTitle.id)

            if newstaff is None:
                return Response('Kişinin bağlı olduğum birimde yönetici bulunmamaktadır.',
                                status=status.HTTP_404_NOT_FOUND)
            personel = Person.objects.get(id=newstaff.Person.id)
            if personel.id == id:
                if organization.UpperOrganization.id is None:
                    serializer = PersonSerializer(personel)
                    data = {}
                    data['id'] = serializer.data['id']
                    data['FullName'] = serializer.data['Name'] + ' ' + serializer.data['Surname']
                    return Response(data)
                staffs = Staff.objects.filter(Organization=organization.UpperOrganization.id)
                if len(staffs) == 0:
                    return Response('Kişinin bağlı olduğu birimde yönetici bulunmamaktadır.',
                                    status=status.HTTP_404_NOT_FOUND)
                personel = Person.objects.get(id=staffs[0].Person.id)
                serializer = PersonSerializer(personel)
                data = {}
                data['id'] = serializer.data['id']
                data['FullName'] = serializer.data['Name'] + ' ' + serializer.data['Surname']
                return Response(data)
            serializer = PersonSerializer(personel)
            data = {}
            data['id'] = serializer.data['id']
            data['FullName'] = serializer.data['Name'] + ' ' + serializer.data['Surname']
            return Response(data)
            # staffs = Staff.objects.get(Organization = organization.UpperOrganization.id)
            # personel = Person.objects.get(id=staffs.Person.id)
            # serializer = PersonSerializer(personel)
            # data = {}
            # data['id'] = serializer.data['id']
            # data['FullName'] = serializer.data['Name'] + ' ' + serializer.data['Surname']
            # return Response(data)

    except:
        return Response("Kadro Bulunamadı", status=status.HTTP_404_NOT_FOUND)


def GetPersonApprover(id):
    staff = Staff.objects.get(Person=id)
    organization = Organization.objects.get(id=staff.Organization.id)
    if organization.CanApproveRight:
        if organization.ManagerTitle == None:
            return Response('Kişinin bağlı olduğu birimde yönetici bulunmamaktadır.', status=status.HTTP_404_NOT_FOUND)

        ystaff = Staff.objects.get(Organization=organization.id, Title=organization.ManagerTitle.id)

        if ystaff == None:
            return Response('Kişinin bağlı olduğu birimde yönetici bulunmamaktadır.', status=status.HTTP_404_NOT_FOUND)
        personel = Person.objects.get(id=ystaff.Person.id)
        if personel.id == id:
            staffs = Staff.objects.get(Organization=organization.UpperOrganization.id)
            personel = Person.objects.get(id=staffs.Person.id)
            serializer = PersonSerializer(personel)
            # data = {}
            # data['id'] = serializer.data['id']
            # data['FullName'] = serializer.data['Name'] + ' ' + serializer.data['Surname']
            return serializer
        serializer = PersonSerializer(personel)
        # data = {}
        # data['id'] = serializer.data['id']
        # data['FullName'] = serializer.data['Name'] + ' ' + serializer.data['Surname']
        return serializer
    else:
        neworganization = Organization.objects.get(id=organization.UpperOrganization.id)
        if neworganization.CanApproveRight:
            newstaff = Staff.objects.get(Organization=neworganization.id, Title=neworganization.ManagerTitle.id)

        if newstaff == None:
            return Response('Kişinin bağlı olduğum birimde yönetici bulunmamaktadır.', status=status.HTTP_404_NOT_FOUND)
        personel = Person.objects.get(id=newstaff.Person.id)
        if personel.id == id:
            staffs = Staff.objects.get(Organization=organization.UpperOrganization.id)
            personel = Person.objects.get(id=staffs.Person.id)
            serializer = PersonSerializer(personel)
            # data = {}
            # data['id'] = serializer.data['id']
            # data['FullName'] = serializer.data['Name'] + ' ' + serializer.data['Surname']
            return serializer
        serializer = PersonSerializer(personel)
        # data = {}
        # data['id'] = serializer.data['id']
        # data['FullName'] = serializer.data['Name'] + ' ' + serializer.data['Surname']
        return serializer

        # staff = Staff.objects.get(Person = id)
        # organization = Organization.objects.get(id = staff.Organization.id)
        # if organization.CanApproveRight:
        #     personel = Person.objects.get(id=id)
        #     serializer = PersonSerializer(personel)
        # else:
        #     staffs = Staff.objects.get(Organization = organization.UpperOrganization.id)
        #     personel = Person.objects.get(id=staffs.Person.id)
        #     serializer = PersonSerializer(personel)

        # return serializer


@api_view(['GET'])
def bornTodayPerson(request):
    try:
        today = datetime.now()
        day = today.day
        month = today.month

        personidentities = PersonIdentity.objects.filter(BirthDate__day=day, BirthDate__month=month)
        persons = []

        finallyData = []
        if len(personidentities) > 0:

            for personIdenty in personidentities:
                data = {}
                person = Person.objects.get(id=personIdenty.Person_id)
                data['Name'] = person.Name
                data['Surname'] = person.Surname
                data['Email'] = person.Email
                data['BirthDate'] = personIdenty.BirthDate
                try:
                    staff = Staff.objects.get(Person=int(personIdenty.Person_id))
                    organization = Organization.objects.get(id=staff.Organization.id)
                    title = Title.objects.get(id=staff.Title_id)
                    data['Organization'] = organization.Name
                    data['Title'] = title.Name
                    finallyData.append(data)
                except:
                    data['Organization'] = ''
                    data['Title'] = ''
                    finallyData.append(data)

        return Response(finallyData)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def bornMonthPerson(request):
    try:
        today = datetime.now()
        month = today.month

        personidentities = PersonIdentity.objects.filter(BirthDate__month=month)
        persons = []

        finallyData = []
        if len(personidentities) > 0:
            for personIdenty in personidentities:
                data = {}
                person = Person.objects.get(id=personIdenty.Person_id)
                data['Name'] = person.Name
                data['Surname'] = person.Surname
                data['Email'] = person.Email
                data['BirthDate'] = personIdenty.BirthDate
                try:
                    staff = Staff.objects.get(Person=int(personIdenty.Person_id))
                    organization = Organization.objects.get(id=staff.Organization.id)
                    title = Title.objects.get(id=staff.Title_id)
                    data['Organization'] = organization.Name
                    data['Title'] = title.Name
                    finallyData.append(data)
                except:
                    data['Organization'] = ''
                    data['Title'] = ''
                    finallyData.append(data)

        return Response(finallyData)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
