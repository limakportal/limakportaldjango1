from .models import Right
from .serializer import RightSerializer , RightWithApproverSerializer
from ..righttype.models import RightType
from ..rightleave.models import RightLeave
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from django.db.models import Sum
from ..utils.enums import EnumRightTypes,EnumRightStatus
from ..organization.models import Organization
from ..staff.models import Staff
from ..person.models import Person
import datetime
from docxtpl import DocxTemplate
from ..person.models import Person
from .serializer import PersonSerializer
from ..businessrules.views import mail_yolla
from ..businessrules.views import GetResponsibleIkPersons , IsManager
from ..person.businesrules import GetPersonApprover
from ..personbusiness.models import PersonBusiness
from ..businessrules.views import GetResponsiblePersonDetails, HasPermission
from ..title.models import Title
from django.db.models import Q
from ..vocationdays.models import VocationDays

from ..businessrules.serializer import OrganizationWithPersonTreeSerializer



class RightAPIView(APIView):
    def get(self,request):
        rights = Right.objects.all().order_by('id')
        serializer = RightSerializer(rights,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = RightSerializer(data = request.data)
        if serializer.is_valid():
            result = RightController(serializer.validated_data)
            if result != "":
                return Response(result,status=status.HTTP_404_NOT_FOUND)
            serializer.save()               
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RightDetails(APIView):

    def get_object(self,id):
        try:
            return Right.objects.get(id=id)
        except Right.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        right = self.get_object(id)
        serializer = RightSerializer(right)
        return Response(serializer.data)


    def put(self, request,id):
        right = self.get_object(id)
        serializer = RightSerializer(right, data=request.data)
        if serializer.is_valid():
            serializer.save()
            if  serializer.data['RightStatus'] == EnumRightStatus.Onaylandi:
                person = Person.objects.get(id = serializer.data['Person'])
                personSerializer = PersonSerializer(person)
                baslik = 'İzin Kullanım Hakkında'
                icerik = 'İzin talebiniz onaylanmıştır. Bakiyenizden ' + str(request.data['RightNumber']) + ' gün düşülmüştür. İzin sürecinizin tamamlanması için imzalı izin formunuzu izne ayrılmadan önce İnsan Kaynakları Direktörlüğüne iletiniz.'
                mail_yolla(baslik,icerik,personSerializer.data['Email'],[personSerializer.data['Email']])
                
                IKPersons = GetResponsibleIkPersons()
                if IKPersons != None:

                    for i in IKPersons:
                        if i['Email'] != "":
                            baslik = 'İzin Kullanım Hakkında'
                            icerik = personSerializer.data['Name'] + ' ' + personSerializer.data['Surname'] + ' in ' + str(serializer.validated_data['StartDate'].date()) + '/' + str(serializer.validated_data['EndDate'].date()) + ' tarihleri arasındaki izni onaylanmıştır.'
                            mail_yolla(baslik,icerik,i['Email'],[i['Email']])

            elif  serializer.data['RightStatus'] == EnumRightStatus.Reddedildi:
                person = Person.objects.get(id = serializer.data['Person'])
                personSerializer = PersonSerializer(person)
                baslik = 'İzin Kullanım Hakkında'
                icerik = 'İzin talebiniz reddedilmiştir.'
                mail_yolla(baslik,icerik,personSerializer.data['Email'],[personSerializer.data['Email']])
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        right = self.get_object(id)
        right.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RightWithApproverAPIView(APIView):
    def get(self,request):
        rights = Right.objects.all().order_by('id')
        serializer = RightWithApproverSerializer(rights,many=True)
        return Response(serializer.data)

class RightDownloadApiView(APIView):
    def get(self,request,id):    
        try:
            right = Right.objects.get(id=id)
            righttype = RightType.objects.get(id=right.RightType.id)
            person = Person.objects.get(id=right.Person.id)
            serializer = GetPersonApprover(person.id)

            if  righttype.RightMainType.id == EnumRightTypes.Yillik:
                filename = 'Yillik_izin_Formu.docx'
                outputfile = "YillikResult.docx"
            if  righttype.RightMainType.id == EnumRightTypes.Mazeret:
                filename = 'Mazeret_izin_Formu.docx'
                outputfile = "MazeretResult.docx"
            if  righttype.RightMainType.id == EnumRightTypes.Ucretsiz:
                filename = 'Ucretsiz_izin_formu.docx'
                outputfile = "UcretsizResult.docx"

            doc = DocxTemplate(filename)
            total = GetRightBalance(id)

            context = { 'Name' : person.Name , 'Surname' : person.Surname , 'No' : right.RightNumber , 'GetDate' : datetime.date.today(),
                         'SD' : right.StartDate.date() , 'EndDate' : right.EndDate.date(),
                         'AppName' : serializer.data['Name'], 'AppSurname' : serializer.data['Surname'],
                         'RD' : right.DateOfReturn.date(), 'Tel' : right.Telephone ,
                         'Bak' : total , 'Kal' : total - right.RightNumber }
            doc.render(context)
            doc.save(outputfile)

            newfile = open(outputfile,'rb')
            response = HttpResponse(FileWrapper(newfile), content_type='application/docx')
            response['Content-Disposition'] = 'filename="result.docx"'
            return response
        except Right.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def RightBalance(request,id):
    try:
        total = GetRightBalance(id)
        return Response({'total' : total})
    except RightLeave.DoesNotExist:
        return Response('Kişiye ait izin hakedişi bulunmamaktadır.',status=status.HTTP_404_NOT_FOUND)

def GetRightBalance(id):
        try:
            rightleave =  RightLeave.objects.filter(Person=id)
            if rightleave:
                leave =  rightleave.aggregate(total=Sum('Earning'))
                right  = Right.objects.filter(Person=id,RightStatus=EnumRightStatus.Onaylandi)
                number = 0
                if  right:
                    for r in right:
                      number +=  r.RightNumber
                total = leave['total'] - number
            else:
                return 0
            return total
        except RightLeave.DoesNotExist:
            return 0

@api_view(['POST'])
def RightDaysNumber(request):
    result = {}
    stardate = datetime.datetime.strptime(request.data['StartDate'],'%Y-%m-%d')
    enddate = datetime.datetime.strptime(request.data['EndDate'],'%Y-%m-%d')
    startime = request.data['StartTime']
    endtime = request.data['EndTime']
    righttypeid = request.data['RightType']
    personid = int(request.data['Person'])
    righttype = RightType.objects.get(id = righttypeid)
    delta = datetime.timedelta(days=1)
    number = tmp = 0
    staff = Staff.objects.filter(Person=personid)
    vdays = VocationDays.objects.all()
    if len(staff) > 0:
        organization = Organization.objects.filter(id=staff[0].Organization.id)
        if  len(organization) > 0:
            while stardate <= enddate:
                days = vdays.filter(DateDay__date = stardate)
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
            return Response('Şirket tanımı yapılmamıştır.',status=status.HTTP_404_NOT_FOUND)
    else:
        return Response('Kadro tanımı yapılmamıştır.',status=status.HTTP_404_NOT_FOUND)
        
    if righttypeid == EnumRightTypes.Yillik:
        content = GetPersonRightInfo(personid)
        contentleave = content['remainingleave']
        contentleave = contentleave + 7 
        if number > contentleave:
            return Response('Yıllık izin bakiyeniz yetersiz. Tekrar kontrol ediniz.',status=status.HTTP_404_NOT_FOUND)

    elif righttype.MaxDayOff != None and righttype.MaxDayOff>0:
        if number > righttype.MaxDayOff:
            return Response('Maksimum izin gün sayısını geçtiniz. Lütfen izin tarihlerinizi kontrol ediniz.', status=status.HTTP_404_NOT_FOUND) 

    if number <= 0:
        return Response('İzin tarihlerini kontrol ediniz.',status=status.HTTP_404_NOT_FOUND)

    result['daynumber'] = number
    if endtime == "12.00":
        result['DateOfReturn'] = enddate
    else:
        result['DateOfReturn'] = stardate

    return   Response(result)

@api_view(['GET'])
def PersonRightInfo(request,id):
        content = []

        if HasPermission(id,'ADMIN'):
            person = Person.objects.all()
            for p in person:
               result = GetPersonRightInfo(p.id)
               content.append(result)
            return Response(content)

        elif HasPermission(id,'IZN_IK'):

            person = Person.objects.get(id = id)
            staff = Staff.objects.get(Person_id = person.id)

            organizationObj = Organization.objects.get(id = staff.Organization_id)
            serializer = OrganizationWithPersonTreeSerializer(organizationObj)
            responsibleMenu = serializer.data

            persons = []

            sameStaffs =  Staff.objects.filter(Organization = staff.Organization_id)
            for staff in sameStaffs:
                try:
                    person = Person.objects.get(id = staff.Person_id)
                    persons.append(person)
                except:
                    person = None

            if responsibleMenu['ChildOrganization'] != None:
                for child in responsibleMenu['ChildOrganization']:
                    staffs = Staff.objects.filter(Organization = child['id'])
                    for staff in staffs:
                        try:
                            person = Person.objects.get(id = staff.Person_id)
                            persons.append(person)
                        except:
                            person = None

            person = Person.objects.all()
            for p in persons:
               result = GetPersonRightInfo(p.id)
               content.append(result)
            return Response(content)

        if IsManager(id):
            staff = Staff.objects.get(Person_id = id)
            staffs = Staff.objects.filter(Organization_id = staff.Organization_id)
            for staff in staffs:
                try:
                    person = Person.objects.get(id = staff.Person_id)
                    result = GetPersonRightInfo(person.id)
                    content.append(result)

                except :
                    pass

            return Response(content)

        result = GetPersonRightInfo(id)
        content.append(result)
        x,responsePersons,y = GetResponsiblePersonDetails(id)
        if responsePersons != None:
            for person in responsePersons:
                result = GetPersonRightInfo(person["Person"]["id"])
                content.append(result)
        return Response(content)

def GetPersonRightInfo(id):
        totalleave = totalright = remainingleave = nextyear = nextleave = approvelwaiting = rightnumber = organiaztion_id = rightwaitingnumber =  0
        registerno = jobstartdate = formerseniority = ""
        rightleave =  RightLeave.objects.filter(Person=id) 
        if rightleave:
            totalleave = rightleave.aggregate(total=Sum('Earning'))['total']
        
        rightapprove = Right.objects.filter(Person=id,RightStatus=EnumRightStatus.Onaylandi,RightType = EnumRightTypes.Yillik)
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
        
        rightwaiting = Right.objects.filter(Person=id,RightStatus=EnumRightStatus.OnayBekliyor)
        if rightwaiting:
            for r in rightwaiting:
              approvelwaiting += r.RightNumber  

        remainingleave = totalleave - totalright - approvelwaiting
        
        person = Person.objects.get(id=id)
        staff = Staff.objects.filter(Person=id)
        if len(staff) > 0:
             organiaztion = Organization.objects.filter(id=staff[0].Organization.id)
             if len(organiaztion) > 0:
                 organiaztion_id = organiaztion[0].id
        
        detail = []
        for item in rightleave:
           for r in rightapprove:
               if r.StartDate.year == item.Year :
                  rightnumber += r.RightNumber
           for r in rightwaiting:
               if r.StartDate.year == item.Year :
                  rightwaitingnumber += r.RightNumber

           det = {'year' : item.Year , 'rightleave' : item.Earning , 'rightnumber': rightnumber, 'remaining' : item.Earning - rightnumber, 'personid': item.Person_id, 'rightleaveid': item.id,
                  'approvelwaiting' : rightwaitingnumber}
           detail.append(det)
           rightnumber = 0
           rightwaitingnumber = 0
      
        content = {'person_id' : person.id, 'name' : person.Name , 'surname': person.Surname,'totalleave' : totalleave, 'totalright': totalright, 'remainingleave' : remainingleave,
                'nextyear' : nextyear, 'nextleave': nextleave, 'approvelwaiting' : approvelwaiting, 'organization_id' : organiaztion_id, 'detail' : detail, 
                'RegisterNo' : registerno , 'JobStartDate': jobstartdate, 'FormerSeniority': formerseniority}
        return content

@api_view(['GET'])
def GetRightStatus(request,status_id):
        try:
            rights = Right.objects.filter(RightStatus = status_id)
            if rights:
                serializer = RightWithApproverSerializer(rights,many=True)
                return Response(serializer.data)
            else:
                return Response('İzin bulunamadı',status=status.HTTP_404_NOT_FOUND)

        except:
           return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def TodayOnLeavePerson(request):
        try:
            today = datetime.date.today()       
            rights = Right.objects.filter(StartDate__day = today.day, StartDate__month = today.month, StartDate__year = today.year)
        
            persons = []
        
            finallyData = []
            for right in rights:
                data = {}
                person = Person.objects.get(id = right.Person_id)
                data['Name'] = person.Name 
                data['Surname'] = person.Surname
                data['Email'] = person.Email
                data['StartDate'] = right.StartDate.date()
                data['EndDate'] = right.EndDate.date()
                data['RightNumber'] = right.RightNumber
                data['RightType'] = EnumRightTypes(right.RightType_id).name
                try:
                    staff = Staff.objects.get(Person=int(person.id))
                    organization = Organization.objects.get(id = staff.Organization_id)
                    title = Title.objects.get(id = staff.Title_id)
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


def RightController(data):
    try:
        sonucmessage = ""
        if data:
            today = datetime.date.today()
            startdate = data['StartDate'].date()
            enddate = data['EndDate'].date()
            personid = int(data['Person'].id)
            righttypeid = int(data['RightType'].id)
            rightnumber = data['RightNumber']
            personapprover = data['Approver1']
            endPrior = datetime.datetime.min.date()
            currentrights = []

            if personid == personapprover:
                sonucmessage = "İzin giren personel ile yönetici aynı kişi olamaz."
                return sonucmessage

            if startdate < today or startdate > enddate or rightnumber <= 0:
                sonucmessage = "İzin tarihlerini kontrol ediniz."
                return sonucmessage

            righttype = RightType.objects.get(id = righttypeid)
            rights = Right.objects.filter(Q(Person = personid) & (Q(RightStatus = EnumRightStatus.Onaylandi) | Q(RightStatus = EnumRightStatus.OnayBekliyor)))  
            for iright in rights:
                currentrights.append([iright.StartDate.date(),iright.EndDate.date()])
        
            currentrights.append([startdate,enddate])
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
                
            if righttypeid == EnumRightTypes.Yillik:
                content = GetPersonRightInfo(personid)
                contentleave = content['remainingleave']
                contentleave = contentleave + 7
                if rightnumber > contentleave:
                    sonucmessage = "Yıllık izin bakiyeniz yetersiz. Tekrar kontrol ediniz."
                    return sonucmessage

            elif righttype.MaxDayOff != None and righttype.MaxDayOff>0:
                if rightnumber > righttype.MaxDayOff:
                    sonucmessage = "Maksimum izin gün sayısını geçtiniz. Lütfen izin tarihlerinizi kontrol ediniz."
                    return sonucmessage
            
            
        return sonucmessage
    except:
        Response("",status=status.HTTP_404_NOT_FOUND)

