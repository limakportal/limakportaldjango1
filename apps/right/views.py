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
from ..person.businesrules import GetPersonApprover

class RightAPIView(APIView):
    def get(self,request):
        rights = Right.objects.all().order_by('id')
        serializer = RightSerializer(rights,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = RightSerializer(data = request.data)
        if serializer.is_valid():
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
                icerik = 'İzin talebiniz onaylanmıştır. Bakiyenizden ' + str(request.data['RightNumber']) + ' gün düşülmüştür.'
                mail_yolla(baslik,icerik,personSerializer.data['Email'],[personSerializer.data['Email']])
            elif  serializer.data['RightStatus'] == EnumRightStatus.Iptal:
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
            context = { 'Name' : person.Name , 'Surname' : person.Surname , 'No' : right.RightNumber , 'GetDate' : datetime.date.today(),
                         'StartDate' : right.StartDate.date() , 'EndDate' : right.EndDate.date(),
                         'ApproveName' : serializer.data['Name'], 'ApproveSurname' : serializer.data['Surname']}
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
        rightleave =  RightLeave.objects.filter(Person=id)
        if rightleave:
            leave =  rightleave.aggregate(total=Sum('Earning'))
            right  = Right.objects.filter(Person=id,RightStatus=EnumRightStatus.Onaylandi)
            number = 0
            if  right:
                number =  right.aggregate(total=Sum('RightNumber'))['total']
            total = leave['total'] - number
        else:
           return Response('Kişiye ait izin hakedişi bulunmamaktadır.',status=status.HTTP_404_NOT_FOUND)
        return Response({'total' : total})
    except RightLeave.DoesNotExist:
        return Response('Kişiye ait izin hakedişi bulunmamaktadır.',status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def RightDaysNumber(request,id):
        stardate = datetime.datetime.strptime(request.data['StartDate'],'%Y-%m-%d')
        enddate = datetime.datetime.strptime(request.data['EndDate'],'%Y-%m-%d')
        startime = request.data['StartTime']
        endtime = request.data['EndTime']
        delta = datetime.timedelta(days=1)
        number = 0
        staff = Staff.objects.get(Person=id)
        if staff:
            organization = Organization.objects.get(id=staff.Organization.id)
            if  organization:
                while stardate < enddate:
                      if stardate.weekday() == 5:
                         if organization.IsSaturdayWorkDay:
                            number +=1
                      elif stardate.weekday() == 6:
                              if organization.IsSundayWorkDay:
                                  number += 1
                      else:
                           number += 1
                      stardate += delta
            else:
                return Response('Şirket tanımı yapılmamıştır.',status=status.HTTP_404_NOT_FOUND)
        else:
            return Response('Kadro tanımı yapılmamıştır.',status=status.HTTP_404_NOT_FOUND)
        
        return   Response({'daynumber' : number})