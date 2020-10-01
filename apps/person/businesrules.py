from datetime import datetime

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializer import PersonSerializer

from ..dashboard.businesrules import GetOrganizationAndUpperOrganization

from .models import Person
from ..organization.models import Organization
from ..personidentity.models import PersonIdentity
from ..personemployment.models import PersonEmployment
from ..staff.models import Staff
from ..title.models import Title


@api_view(['GET'])
def PersonApprover(request, id):
    dataArr = []
    try:
        organization_Arr = []
        staff = Staff.objects.get(Person=id)
        organization_Arr.append(staff.Organization_id)

        try:
            personemployment = PersonEmployment.objects.filter(Person=id)
            if len(personemployment) > 0:
                for pemp in personemployment:
                    if pemp.Organization.id in organization_Arr:
                        break
                    organization_Arr.append(pemp.Organization.id)
        except:
            pass

        for oa in organization_Arr:
            data = GetPersonApprover2(oa, id)
            dataArr.append(data)


    except:
        pass

    return Response(dataArr)


def GetPersonApprover2(organizationId, id):
    global newstaff
    try:
        organization = Organization.objects.get(id=organizationId)
        if organization.CanApproveRight:
            if organization.ManagerTitle is None:
                data = {}
                data['id'] = ""
                data['FullName'] = ""
                return data

            ystaff = Staff.objects.filter(Organization=organization.id, Title=organization.ManagerTitle.id)

            if len(ystaff) == 0:
                data = {}
                data['id'] = ""
                data['FullName'] = ""
                return data
            personel = Person.objects.get(id=ystaff[0].Person.id)
            if personel.id == id:
                staffs = Staff.objects.filter(Organization=organization.UpperOrganization.id)
                if len(staffs) == 0:
                    data = {}
                    data['id'] = ""
                    data['FullName'] = ""
                    return data

                personel = Person.objects.get(id=staffs[0].Person.id)
                data = {}
                data['id'] = personel.id
                data['FullName'] = personel.Name + ' ' + personel.Surname
                return data
            data = {}
            data['id'] = personel.id
            data['FullName'] = personel.Name + ' ' + personel.Surname
            return data
        else:
            neworganization = Organization.objects.get(id=organization.UpperOrganization.id)
            upper_organization_Arr = []
            upper_organization_Arr = GetOrganizationAndUpperOrganization(neworganization.id, upper_organization_Arr)

            for uo in upper_organization_Arr:

                # if neworganization.CanApproveRight:
                if uo.CanApproveRight:
                    newstaff = Staff.objects.filter(Organization=uo.id, Title=uo.ManagerTitle.id)
                    if len(newstaff) == 0:
                        data = {}
                        data['id'] = ""
                        data['FullName'] = ""
                        return data
                    personel = Person.objects.get(id=newstaff[0].Person.id)
                    if personel.id == id:
                        if organization.UpperOrganization.id is None:
                            data = {}
                            data['id'] = personel.id
                            data['FullName'] = personel.Name + ' ' + personel.Surname
                            return data
                        staffs = Staff.objects.filter(Organization=organization.UpperOrganization.id)
                        if len(staffs) == 0:
                            data = {}
                            data['id'] = ""
                            data['FullName'] = ""
                            return data
                        personel = Person.objects.get(id=staffs[0].Person.id)
                        data = {}
                        data['id'] = personel.id
                        data['FullName'] = personel.Name + ' ' + personel.Surname
                        return data
                    serializer = PersonSerializer(personel)
                    data = {}
                    data['id'] = personel.id
                    data['FullName'] = personel.Name + ' ' + personel.Surname
                    return data


    except:
        data = {}
        data['id'] = ""
        data['FullName'] = ""
        return data


def GetPersonApprover(id):
    try:
        staff = Staff.objects.get(Person=id)
        organization = Organization.objects.get(id=staff.Organization.id)
        if organization.CanApproveRight:
            if organization.ManagerTitle == None:
                # return Response('Kişinin bağlı olduğu birimde yönetici bulunmamaktadır.', status=status.HTTP_404_NOT_FOUND)
                return ""

            ystaff = Staff.objects.filter(Organization=organization.id, Title=organization.ManagerTitle.id)

            if len(ystaff) == 0:
                # return Response('Kişinin bağlı olduğu birimde yönetici bulunmamaktadır.', status=status.HTTP_404_NOT_FOUND)
                return ""
            personel = Person.objects.get(id=ystaff[0].Person.id)
            if personel.id == id:
                try:
                    staffs = Staff.objects.get(Organization=organization.UpperOrganization.id)
                    personel = Person.objects.get(id=staffs.Person.id)
                    serializer = PersonSerializer(personel)
                    return serializer
                except:
                    return ""
            serializer = PersonSerializer(personel)
            return serializer
        else:
            neworganization = Organization.objects.get(id=organization.UpperOrganization.id)
            if neworganization.CanApproveRight:
                newstaff = Staff.objects.get(Organization=neworganization.id, Title=neworganization.ManagerTitle.id)
                if newstaff == None:
                    # return Response('Kişinin bağlı olduğum birimde yönetici bulunmamaktadır.', status=status.HTTP_404_NOT_FOUND)
                    return ""
                personel = Person.objects.get(id=newstaff.Person.id)
                if personel.id == id:
                    try:
                        staffs = Staff.objects.get(Organization=organization.UpperOrganization.id)
                        personel = Person.objects.get(id=staffs.Person.id)
                        serializer = PersonSerializer(personel)
                        return serializer
                    except:
                        return ""
                serializer = PersonSerializer(personel)
                return serializer
    except:
        pass

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
