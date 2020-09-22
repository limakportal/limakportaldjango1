import datetime
from wsgiref.util import FileWrapper

import pytz
from django.db import connection
from django.db.models import Q
from django.db.models import Sum
from django.http import HttpResponse
from docxtpl import DocxTemplate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .bussinessrules import GetRightBalance, PersonRightSummary
from .models import Right
from .serializer import PersonSerializer
from .serializer import RightSerializer, RightWithApproverSerializer, RightAllDetailsSerializer2
from ..businessrules.views import GetResponsibleIkPersons, IsManager
from ..businessrules.views import GetResponsiblePersonDetails, HasPermission, GetManagerPersonsDetail, \
    GetManagerOrganizationsDetailNoneSerializer, GetPersonsByOrganizationId
from ..organization.models import Organization
from ..person.businesrules import GetPersonApprover
from ..person.models import Person
from ..personbusiness.models import PersonBusiness
from ..personidentity.models import PersonIdentity
from ..rightleave.models import RightLeave
from ..righttype.models import RightType
from ..staff.models import Staff
from ..title.models import Title
from ..utils.enums import EnumRightTypes, EnumRightStatus, EnumStatus
from ..vocationdays.models import VocationDays

from ..dashboard.businesrules import ListResponsiblePersons



class RightAPIView(APIView):
    def get(self, request):
        rights = Right.objects.all().order_by('id')
        serializer = RightSerializer(rights, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RightSerializer(data=request.data)
        if serializer.is_valid():
            result = RightController(serializer.validated_data, 0)
            if result != "":
                return Response(result, status=status.HTTP_404_NOT_FOUND)
            serializer.save(CreatedBy=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RightDetails(APIView):

    def get_object(self, id):
        try:
            return Right.objects.get(id=id)
        except Right.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        right = self.get_object(id)
        serializer = RightSerializer(right)
        return Response(serializer.data)

    def put(self, request, id):
        right = self.get_object(id)
        serializer = RightSerializer(right, data=request.data)
        if serializer.is_valid():
            result = RightController(serializer.validated_data, id)
            if result != "":
                return Response(result, status=status.HTTP_404_NOT_FOUND)
            serializer.save(ModifiedBy=self.request.user)
            if serializer.data['RightStatus'] == EnumRightStatus.Onaylandi:
                person = Person.objects.get(id=serializer.data['Person'])
                personSerializer = PersonSerializer(person)
                baslik = 'İzin Kullanım Hakkında'
                icerik = 'İzin talebiniz onaylanmıştır. Bakiyenizden ' + str(request.data[
                                                                                 'RightNumber']) + ' gün düşülmüştür. İzin sürecinizin tamamlanması için imzalı izin formunuzu izne ayrılmadan önce İnsan Kaynakları Direktörlüğüne iletiniz.'
                # mail_yolla(baslik,icerik,personSerializer.data['Email'],[personSerializer.data['Email']])

                IKPersons = GetResponsibleIkPersons()
                if IKPersons != None:

                    for i in IKPersons:
                        if i['Email'] != "":
                            baslik = 'İzin Kullanım Hakkında'
                            icerik = personSerializer.data['Name'] + ' ' + personSerializer.data[
                                'Surname'] + ' in ' + str(serializer.validated_data['StartDate'].date()) + '/' + str(
                                serializer.validated_data[
                                    'EndDate'].date()) + ' tarihleri arasındaki izni onaylanmıştır.'
                            # mail_yolla(baslik,icerik,i['Email'],[i['Email']])

            elif serializer.data['RightStatus'] == EnumRightStatus.Reddedildi:
                person = Person.objects.get(id=serializer.data['Person'])
                personSerializer = PersonSerializer(person)
                baslik = 'İzin Kullanım Hakkında'
                icerik = 'İzin talebiniz reddedilmiştir.'
                # mail_yolla(baslik,icerik,personSerializer.data['Email'],[personSerializer.data['Email']])
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        right = self.get_object(id)
        right.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RightWithApproverAPIView(APIView):
    def get(self, request):
        if (request.user.is_authenticated):
            try:
                p = Person.objects.get(Email=request.user.email)
                personArr = ListResponsiblePersons(p.id)
                rightArr = []
                for p in personArr:
                    try:
                        rights = Right.objects.get(Person_id=p.id)
                        rightArr.append(rights)
                    except:
                        pass
                if len(rightArr) > 0:
                    serializer = RightWithApproverSerializer(rightArr, many=True)
                    return Response(serializer.data)
                else:
                    return Response([])


            except:
                return Response([])
        return Response([])


class RightWithApproverDetail(APIView):
    def get(self, request, id):
        rights = Right.objects.filter(Person_id=id)
        if len(rights) > 0:
            serializer = RightWithApproverSerializer(rights, many=True)
            return Response(serializer.data)
        else:
            return Response([])


class RightDownloadApiView(APIView):
    def get(self, request, id):
        try:
            right = Right.objects.get(id=id)
            righttype = RightType.objects.get(id=right.RightType.id)
            person = Person.objects.get(id=right.Person.id)
            personbusiness = PersonBusiness.objects.get(Person=right.Person.id)
            serializer = GetPersonApprover(person.id)

            if righttype.RightMainType.id == EnumRightTypes.Yıllık:
                filename = 'Yillik_izin_Formu.docx'
                outputfile = "YillikResult.docx"
            if righttype.RightMainType.id == EnumRightTypes.Mazeret:
                filename = 'Mazeret_izin_Formu.docx'
                outputfile = "MazeretResult.docx"
            if righttype.RightMainType.id == EnumRightTypes.Ücretsiz:
                filename = 'Ucretsiz_izin_formu.docx'
                outputfile = "UcretsizResult.docx"

            doc = DocxTemplate(filename)
            personsummary = PersonRightSummary(person.id)
            total = personsummary["BalanceRigth"]

            context = {'Name': person.Name, 'Surname': person.Surname, 'No': right.RightNumber,
                       'GetDate': datetime.date.today().strftime('%m-%d-%Y'),
                       'SD': right.StartDate.date().strftime('%m-%d-%Y'), 'EndDate': right.EndDate.date().strftime('%m-%d-%Y'),
                       'AppName': serializer.data['Name'], 'AppSurname': serializer.data['Surname'],
                       'RD': right.DateOfReturn.date().strftime('%m-%d-%Y'), 'Tel': right.Telephone,
                       'Bak': total, 'Kal': total - right.RightNumber, 'JD': personbusiness.JobStartDate.date().strftime('%m-%d-%Y'),
                       'SCNO': personbusiness.RegisterNo,
                       'KIDEM': personsummary["NumberOfDaysSubjestToRight"]}
            doc.render(context)
            doc.save(outputfile)

            newfile = open(outputfile, 'rb')
            response = HttpResponse(FileWrapper(newfile), content_type='application/docx')
            response['Content-Disposition'] = 'filename="result.docx"'
            return response
        except Right.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def ApproveRight(request, id):
    try:
        right = Right.objects.get(id=id)
        getrequest = RightSerializer(right).data
        if getrequest['RightStatus'] == int(EnumRightStatus.Iptal):
            return Response("İptal durumunda olan izin onaylanamaz.", status=status.HTTP_404_NOT_FOUND)
        serializer = RightSerializer(right, data=getrequest)
        serializer.initial_data['RightStatus'] = int(EnumRightStatus.Onaylandi)
        if serializer.is_valid():
            serializer.save(ModifiedBy=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def DenyRight(request, id):
    try:
        right = Right.objects.get(id=id)
        getrequest = RightSerializer(right).data
        if getrequest['RightStatus'] == int(EnumRightStatus.Iptal):
            return Response("İptal durumunda olan izin reddedilemez.", status=status.HTTP_404_NOT_FOUND)
        serializer = RightSerializer(right, data=getrequest)
        serializer.initial_data['RightStatus'] = int(EnumRightStatus.Reddedildi)
        serializer.initial_data['DenyExplanation'] = request.data['DenyExplanation']
        if serializer.is_valid():
            serializer.save(ModifiedBy=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        Response(str(e), status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def HasField(request, id):
    try:
        right = Right.objects.get(id=id)
        getrequest = RightSerializer(right).data
        if getrequest['RightStatus'] != int(EnumRightStatus.Onaylandi):
            return Response("Sadece onaylanan izinler dosyalanabilir.", status=status.HTTP_404_NOT_FOUND)
        if getrequest['HrHasField'] == int(EnumStatus.Active):
            return Response("Seçilen izin dosyalandı durumundadır.", status=status.HTTP_404_NOT_FOUND)
        serializer = RightSerializer(right, data=getrequest)
        serializer.initial_data['HrHasField'] = int(EnumStatus.Active)
        if serializer.is_valid():
            serializer.save(ModifiedBy=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        Response(str(e), status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def RightBalance(request, id):
    try:
        total = GetRightBalance(id)
        return Response({'total': total})
    except RightLeave.DoesNotExist:
        return Response('Kişiye ait izin hakedişi bulunmamaktadır.', status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def RightDaysNumber(request):
    result = {}
    stardate = datetime.datetime.strptime(request.data['StartDate'], '%Y-%m-%d')
    enddate = datetime.datetime.strptime(request.data['EndDate'], '%Y-%m-%d')
    startime = request.data['StartTime']
    endtime = request.data['EndTime']
    righttypeid = request.data['RightType']
    personid = int(request.data['Person'])
    righttype = RightType.objects.get(id=righttypeid)
    delta = datetime.timedelta(days=1)
    number = tmp = 0
    staff = Staff.objects.filter(Person=personid)
    vdays = VocationDays.objects.all()
    if len(staff) > 0:
        organization = Organization.objects.filter(id=staff[0].Organization.id)
        if len(organization) > 0:
            while stardate <= enddate:
                days = vdays.filter(DateDay__date=stardate)
                if len(days) > 0:
                    if days[0].DayType == 0:
                        number += 0.5
                    stardate += delta
                    tmp += 1
                    continue
                if stardate.weekday() == 4:
                    if organization[0].IsSaturdayWorkDay:
                        if tmp == 0:
                            if startime == "13.00":
                                number += 1.5
                            else:
                                number += 2
                        else:
                            number += 2
                        stardate += delta
                        tmp += 1
                if stardate.weekday() == 5:
                    stardate += delta
                    tmp += 1
                    # if organization[0].IsSaturdayWorkDay:
                    #     if tmp == 0:
                    #         if startime == "13.00":
                    #             number += 0.5
                    #         else:
                    #             number += 1
                    #     else:
                    #         number += 1
                elif stardate.weekday() == 6:
                    if organization[0].IsSundayWorkDay:
                        if tmp == 0:
                            if startime == "13.00":
                                number += 0.5
                            else:
                                number += 1
                        else:
                            number += 1
                else:
                    if tmp == 0 and startime == "13.00":
                        number += 0.5
                    else:
                        number += 1
                stardate += delta
                tmp += 1
            if endtime == "12.00":
                if enddate.weekday() == 4:
                    if organization[0].IsSaturdayWorkDay:
                        number -= 1.5
                elif enddate.weekday() == 5:
                    if organization[0].IsSaturdayWorkDay:
                        number -= 0.5
                elif enddate.weekday() == 6:
                    if organization[0].IsSundayWorkDay:
                        number -= 0.5
                else:
                    number -= 0.5
        else:
            return Response('Şirket tanımı yapılmamıştır.', status=status.HTTP_404_NOT_FOUND)
    else:
        return Response('Kadro tanımı yapılmamıştır.', status=status.HTTP_404_NOT_FOUND)

    if righttypeid == EnumRightTypes.Yıllık:
        content = PersonRightSummary(personid)
        contentleave = content['BalanceRigth']
        contentleave = contentleave + 7
        if number > contentleave:
            return Response('Yıllık izin bakiyeniz yetersiz. Tekrar kontrol ediniz.', status=status.HTTP_404_NOT_FOUND)

    elif righttype.MaxDayOff != None and righttype.MaxDayOff > 0:
        if number > righttype.MaxDayOff:
            return Response('Maksimum izin gün sayısını geçtiniz. Lütfen izin tarihlerinizi kontrol ediniz.',
                            status=status.HTTP_404_NOT_FOUND)

    if number <= 0:
        return Response('İzin tarihlerini kontrol ediniz.', status=status.HTTP_404_NOT_FOUND)

    result['daynumber'] = number
    if endtime == "12.00":
        result['DateOfReturn'] = enddate
    else:
        result['DateOfReturn'] = stardate

    return Response(result)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def PersonRightInfo(request, id):
    content = []

    """person admin,ik,manager yetkilerine göre sorumlu olduğu personları getirir"""
    personArr = ListResponsiblePersons(id)
    for p in personArr:
        result = GetPersonRightInfo(p.id)
        content.append(result)
    # return Response(content)

    # x, responsePersons, y = GetResponsiblePersonDetails(id)
    # # liste boş gelirse kendisini ekledim (gokhan) neden yaptım bilmiyorm :d neden listeden boş geliyor.
    # if len(responsePersons) == 0:
    #     responsePersons.append(y)
    # if responsePersons != None:
    #     for person in responsePersons:
    #         result = GetPersonRightInfo(person["Person"]["id"])
    #         content.append(result)
    return Response(content)


@api_view(['GET'])
def PersonRightInfoPerson(request, id):
    content = []
    persons = []
    yetkili = False
    if IsManager(id):
        yetkili = True
        persons = GetManagerPersonsDetail(id)
    else:
        staff = Staff.objects.get(Person_id=id)
        persons = GetPersonsByOrganizationId(staff.Organization_id, persons)

    for p in persons:
        try:
            result = GetPersonRightInfo(p["id"])
            content.append(result)
        except:
            pass

    # Kendisi yukarıda geliyor.
    # result = GetPersonRightInfo(id)
    # content.append(result)
    # ismanager ise zaten alttakiler geliyor. bu yüzden çiftliyor. başka sebeptense ona göre yaparız.
    if yetkili is False:
        x, responsePersons, y = GetResponsiblePersonDetails(id)
        if responsePersons is not None:
            for person in responsePersons:
                result = GetPersonRightInfo(person["Person"]["id"])
                content.append(result)
    return Response(content)


def GetPersonRightInfo(id):
    totalleave = totalright = remainingleave = nextyear = nextleave = approvelwaiting = rightnumber = organiaztion_id = rightwaitingnumber = 0
    registerno = jobstartdate = formerseniority = ""
    rightleave = RightLeave.objects.filter(Person=id)
    if rightleave:
        totalleave = rightleave.aggregate(total=Sum('Earning'))['total']

    rightapprove = Right.objects.filter(Person=id, RightStatus=EnumRightStatus.Onaylandi,
                                        RightType=EnumRightTypes.Yıllık)
    if rightapprove:
        for r in rightapprove:
            totalright += r.RightNumber

    personbusiness = PersonBusiness.objects.filter(Person=id)
    if len(personbusiness) > 0:
        businessyear = personbusiness[0].JobStartDate
        if datetime.date.today().year - businessyear.year >= 5:
            nextleave = 20
        else:
            nextleave = 14

        nextyear = str(datetime.date.today().year + 1) + '-' + str(businessyear.month) + '-' + str(businessyear.day)
        registerno = personbusiness[0].RegisterNo
        jobstartdate = personbusiness[0].JobStartDate
        formerseniority = personbusiness[0].FormerSeniority

    rightwaiting = Right.objects.filter(Person=id, RightStatus=EnumRightStatus.OnayBekliyor)
    if rightwaiting:
        for r in rightwaiting:
            approvelwaiting += r.RightNumber

    remainingleave = totalleave - totalright - approvelwaiting

    person = Person.objects.get(id=id)
    personIdentity = PersonIdentity.objects.filter(Person=id)
    gender = ""
    if len(personIdentity) > 0:
        if personIdentity[0].Gender is not None:
            gender = personIdentity[0].Gender.Name
        else:
            gender = "Tanımlanmamış"
    else:
        gender = "Tanımlanmamış"

    staff = Staff.objects.filter(Person=id)
    organiaztionName = ""
    organiaztionTypeName = ""
    if len(staff) > 0:
        organiaztion = Organization.objects.filter(id=staff[0].Organization.id)
        # title = Title.objects.get(id=staff[0].Title.id)
        if len(organiaztion) > 0:
            organiaztion_id = organiaztion[0].id
            organiaztionName = organiaztion[0].Name
            if organiaztion[0].OrganizationType is not None:
                organiaztionTypeName = organiaztion[0].OrganizationType.Name
            else:
                organiaztionTypeName = ""
            # titleName = title.Name

    detail = []
    for item in rightleave:
        for r in rightapprove:
            if r.StartDate.year == item.Year:
                rightnumber += r.RightNumber
        for r in rightwaiting:
            if r.StartDate.year == item.Year:
                rightwaitingnumber += r.RightNumber

        det = {'year': item.Year, 'rightleave': item.Earning, 'rightnumber': rightnumber,
               'remaining': item.Earning - rightnumber, 'personid': item.Person_id, 'rightleaveid': item.id,
               'approvelwaiting': rightwaitingnumber}
        detail.append(det)
        rightnumber = 0
        rightwaitingnumber = 0

    try:
        personRightSummary = PersonRightSummary(person.id)
    except:
        personRightSummary = None

    content = {'person_id': person.id, 'name': person.Name, 'surname': person.Surname,
               'organization_id': organiaztion_id, 'detail': detail,
               'RegisterNo': registerno, 'JobStartDate': jobstartdate, 'FormerSeniority': formerseniority,
               'PersonRightSummary': personRightSummary,
               'Organization': organiaztionName,
               "OrganizationType": organiaztionTypeName,
               "Gender": gender}
            #    , "Title": titleName}
    return content


@api_view(['GET'])
def GetRightStatus(request, status_id):
    try:
        rights = Right.objects.filter(RightStatus=status_id)
        if rights:
            serializer = RightWithApproverSerializer(rights, many=True)
            return Response(serializer.data)
        else:
            return Response('İzin bulunamadı', status=status.HTTP_404_NOT_FOUND)

    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def TodayOnLeavePerson(request):
    try:
        today = datetime.date.today()
        rights = Right.objects.filter(StartDate__day=today.day, StartDate__month=today.month,
                                      StartDate__year=today.year)

        persons = []

        finallyData = []
        for right in rights:
            data = {}
            person = Person.objects.get(id=right.Person_id)
            data['Name'] = person.Name
            data['Surname'] = person.Surname
            data['Email'] = person.Email
            data['StartDate'] = right.StartDate.date()
            data['EndDate'] = right.EndDate.date()
            data['RightNumber'] = right.RightNumber
            try:
                data['RightType'] = RightType.objects.get(id=right.RightType_id).Name
            except:
                data['RightType'] = None
            try:
                staff = Staff.objects.get(Person=int(person.id))
                organization = Organization.objects.get(id=staff.Organization_id)
                title = Title.objects.get(id=staff.Title_id)
                data['Organization'] = organization.Name
                data['Title'] = title.Name
                # finallyData.append(data)
            except:
                data['Organization'] = ''
                data['Title'] = ''
                # finallyData.append(data)
            try:
                data['PersonRightSummary'] = PersonRightSummary(person.id)
            except:
                data['PersonRightSummary'] = None
            finallyData.append(data)

        return Response(finallyData)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def TodayOnLeavePersonByPerson(request, id):
    try:
        today = datetime.date.today()
        organizationarr = GetManagerOrganizationsDetailNoneSerializer(id)
        liste = []
        for o in organizationarr:
            liste.append(str(o.id))
            deger = ",".join(liste)
        rows = TodayOnLeaveByOrganizatinID(deger)
        persons = []

        finallyData = []
        for row in rows:
            data = {}
            data['Name'] = row[0]
            data['Surname'] = row[1]
            data['Email'] = row[2]
            data['StartDate'] = row[12].date()
            data['EndDate'] = row[4].date()
            data['RightNumber'] = row[8]
            try:
                data['RightType'] = RightType.objects.get(id=row[13]).Name
            except:
                data['RightType'] = None
            data['Organization'] = row[17]
            data['Title'] = row[22]
            data['Manager'] = row[23]
            data['DateOfReturn'] = row[5]
            try:
                data['PersonRightSummary'] = PersonRightSummary(id)
            except:
                data['PersonRightSummary'] = None
            finallyData.append(data)

        return Response(finallyData)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


def RightController(data, rightid):
    try:
        sonucmessage = ""
        if data:
            today = datetime.datetime.utcnow()
            today = today.replace(tzinfo=pytz.utc)
            startdate = data['StartDate']
            enddate = data['EndDate']
            personid = int(data['Person'].id)
            righttypeid = int(data['RightType'].id)
            rightnumber = data['RightNumber']
            personapprover = data['Approver1']
            endPrior = datetime.datetime.min
            endPrior = endPrior.replace(tzinfo=pytz.utc)
            currentrights = []

            righttype = RightType.objects.get(id=righttypeid)
            rights = Right.objects.filter(Q(Person=personid) & ~Q(id=rightid) & (
                    Q(RightStatus=EnumRightStatus.Onaylandi) | Q(RightStatus=EnumRightStatus.OnayBekliyor)))
            for iright in rights:
                currentrights.append([iright.StartDate, iright.EndDate])

            if personid == personapprover:
                sonucmessage = "İzin giren personel ile yönetici aynı kişi olamaz."
                return sonucmessage

            if startdate < today or startdate > enddate or rightnumber <= 0:
                sonucmessage = "İzin tarihlerini kontrol ediniz."
                return sonucmessage

            currentrights.append([startdate, enddate])
            count = 0
            # currentrights = sorted(currentrights,key=lambda x: x[0])
            currentrights = sorted(currentrights)
            for r in currentrights:
                if r[0] > r[1]:
                    count = count + 1
                if r[0] < endPrior:
                    count = count + 1
                endPrior = r[1]
            if count > 0:
                sonucmessage = "Seçilen tarihler arası izin bulunmaktadır."
                return sonucmessage

            if righttypeid == EnumRightTypes.Yıllık:
                content = PersonRightSummary(personid)
                contentleave = content['BalanceRigth']
                contentleave = contentleave + 7
                if rightnumber > contentleave:
                    sonucmessage = "Yıllık izin bakiyeniz yetersiz. Tekrar kontrol ediniz."
                    return sonucmessage

            elif righttype.MaxDayOff != None and righttype.MaxDayOff > 0:
                if rightnumber > righttype.MaxDayOff:
                    sonucmessage = "Maksimum izin gün sayısını geçtiniz. Lütfen izin tarihlerinizi kontrol ediniz."
                    return sonucmessage

        return sonucmessage
    except Exception as e:
        Response(str(e), status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def RightAllDetails(request):
    rights = Right.objects.all().order_by('Person_id')
    serializer = RightAllDetailsSerializer2(rights, many=True)
    # persons = []
    # for right in rights:
    #     try:
    #         person = Person.objects.get(id = right.Person_id)
    #         if person not in persons:                  
    #             persons.append(person)
    #     except :
    #         pass

    # serializer = RightAllDetailsSerializer(persons,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def RightSummary(request, id):
    try:
        result = PersonRightSummary(id)
    except:
        result = None
    return Response(result)


def TodayOnLeaveByOrganizatinID(organizationID):
    try:
        with connection.cursor() as cursor:
            query = """
            select p."Name",p."Surname",p."Email", r.*, o."Name", t."Name",
            concat(pm."Name" ,' ',pm."Surname") as Manager
            from "Right" r
            inner join "Person" p on p.id = r."Person_id"
            inner join "Staff" s on p.id = s."Person_id"
            inner join "Organization" o on o.id = s."Organization_id"
            inner join "Title" t on t.id = s."Title_id"
            inner  join "Staff" sm on sm."Title_id" = "ManagerTitle_id" and sm."Organization_id" = s."Organization_id"
            inner  join "Person" pm on pm.id = sm."Person_id"
            where s."Organization_id" in (""" + organizationID + """) AND date_part('MONTH', now()) = date_part('MONTH', r."StartDate")
            AND date_part('YEAR', now()) = date_part('YEAR', r."StartDate") AND date_part('DAY', now()) = date_part('DAY', r."StartDate");
            
            """
            cursor.execute(query)
            row = cursor.fetchall()
        return row
    except Exception as e:
        return e
