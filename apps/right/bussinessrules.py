import datetime
from datetime import timedelta
from django.db.models import Sum
from ..utils.enums import EnumRightTypes,EnumRightStatus

from ..personbusiness.models import PersonBusiness

from ..rightleave.models import RightLeave

from .models import Right


def WorkedTotalDays(personId):
    try:
        personBusiness = PersonBusiness.objects.get(Person_id = personId)
        dToday = datetime.datetime.now()
        today =  datetime.date(dToday.year,dToday.month,dToday.day)
        getJobStartDate = datetime.date(personBusiness.JobStartDate.year,personBusiness.JobStartDate.month,personBusiness.JobStartDate.day)
        dayDifference = (today - getJobStartDate).days + personBusiness.FormerSeniority
        if dayDifference < 1:
            dayDifference = 0
    except:
        return 0
    return dayDifference

def PersonDeserveRight(personId):
    try:
        daysDifference = WorkedTotalDays(personId)
        workingYear = 0
        totalRigts = 0
        if daysDifference > 359:
            workingYear = daysDifference//360
        if workingYear < 5:
            totalRigts = workingYear * 14
        elif workingYear > 4 and workingYear < 15:
            totalRigts = workingYear * 20
        else:
            totalRigts = workingYear * 26
    except:
        return 0
    return totalRigts

def TotalWorkedTime(personId):
    try:
        dayDifference = WorkedTotalDays(personId)
        workedYear = 0
        if dayDifference > 359:
            workedYear = dayDifference // 360
        workedMounth = 0
        if dayDifference > 29:
            workedMounth = (dayDifference - (workedYear * 360)) // 30
        workedDay = 0
        if dayDifference > 0:
            workedDay = dayDifference - ((workedYear * 360) + (workedMounth * 30))
        totalWorkedTime = ''
        if workedYear > 0:
           totalWorkedTime = totalWorkedTime +str(workedYear) + ' Yıl '
        if workedMounth > 0:
            totalWorkedTime = totalWorkedTime + str(workedMounth) + ' Ay '
        if workedDay > 0:
            totalWorkedTime = totalWorkedTime + str(workedDay) + ' Gün'
    except :
        return ''
    return totalWorkedTime

def NextRightTime(personId):
    try:
        personWorkedTotalDays = WorkedTotalDays(personId)
        personWorkedTotalYears = personWorkedTotalDays // 360
        nextRightDay = 360 - (personWorkedTotalDays - (personWorkedTotalYears * 360))
        nextRightDate = datetime.datetime.now() + timedelta(nextRightDay )
        nextRight = str(nextRightDate.year) + '-' + str(nextRightDate.month) + '-' + str(nextRightDate.day) 
    except :
        return ''
    return nextRight


def NextRight(personId):
    try:
        daysDifference = WorkedTotalDays(personId)
        workingYear = 0
        right = 0
        if daysDifference > 359:
            right = daysDifference//360
        if workingYear < 5:
            right =  14
        elif workingYear > 4 and workingYear < 15:
            right =  20
        else:
            right =  26
    except:
        return 0
    return right
 

def PersonRightDeverse(personId):
    result = {}
    right  = Right.objects.filter(Person=personId,RightStatus=EnumRightStatus.Onaylandi,RightType= EnumRightTypes.Yillik)
    number = 0
    if  right:
        for r in right:
            number +=  r.RightNumber
    result['BalanceRigth'] = PersonDeserveRight(personId) - number
    result['TotalWorkedTime'] = TotalWorkedTime(personId)
    result['NextRightTime'] = NextRightTime(personId)
    result['PersonDeserveRight'] = PersonDeserveRight(personId)
    result['NextRight'] = NextRight(personId)
    return result

    

def GetRightBalance(id):
        try:
            rightleave =  RightLeave.objects.filter(Person=id)
            if rightleave:
                leave =  rightleave.aggregate(total=Sum('Earning'))
                right  = Right.objects.filter(Person=id,RightStatus=EnumRightStatus.Onaylandi,RightType= EnumRightTypes.Yillik)
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