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

        totalYear = 0
        totalMounth = 0
        totalDay = 0
        if today.month > getJobStartDate.month or today.month == getJobStartDate.month:
            totalYear = today.year - getJobStartDate.year
            totalMounth = today.month - getJobStartDate.month
            totalDay = abs(today.day - getJobStartDate.day)

        else:
            totalYear = today.year - getJobStartDate.year -1
            totalMounth = today.month
            totalDay = abs(today.day - getJobStartDate.day)
        oldYear = (personBusiness.FormerSeniority // 360)
        oldMounth = (personBusiness.FormerSeniority - (oldYear*360)) // 30
        oldDay = personBusiness.FormerSeniority - ((oldYear*360) +  oldMounth*30)

        totalDay = totalDay + oldDay 

        if oldDay > 29:
            totalMounth = totalMounth + 1
            totalDay = totalDay + oldDay - 30

        totalMounth = totalMounth + oldMounth

        if oldMounth > 11:
            totalYear = totalYear + 1
            totalMounth = totalMounth + oldMounth - 12

        totalYear = totalYear + oldYear
        dayDifference = (totalYear *360 ) + (totalMounth *30) + (totalDay)    
        if dayDifference < 1:
            dayDifference = 0
    except:
        return 0
    return dayDifference

def TotalDeservedRight(personId):
    try:
        totalleave = 0
        rightleave = RightLeave.objects.filter(Person_id = personId)
        if len(rightleave) > 0:
            totalleave = rightleave.aggregate(total=Sum('Earning'))['total']
        
        # workingYear = 0
        # totalRigts = 0
        # if daysDifference > 359:
        #     workingYear = daysDifference//360
        # if workingYear <= 5:
        #     totalRigts = workingYear * 14
        # elif workingYear > 5 and workingYear <= 15:
        #     totalRigts = 14 * 5 + (workingYear - 5) * 20
        # else:
        #     totalRigts = 14 * 5 + 10 * 20 + (workingYear - 15) * 26
    except:
        return 0
    return totalleave

def NumberOfDaysSubjestToRight(personId,dayDifference):
    try:
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

def NextRighNumberOfDaysSubjestToRighttTime(personId , dayDifference):
    try:
        personWorkedTotalDays = dayDifference
        personWorkedTotalYears = personWorkedTotalDays // 360
        nextRightDay = 360 - (personWorkedTotalDays - (personWorkedTotalYears * 360))
        nextRightDate = datetime.datetime.now() + timedelta(nextRightDay )
        nextRight = str(nextRightDate.year) + '-' + str(nextRightDate.month) + '-' + str(nextRightDate.day) 
    except :
        return ''
    return nextRight


def RightToBeDeserved(personId,dayDifference):
    try:
        daysDifference = dayDifference
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
 

def PersonRightSummary(personId):
    result = {}

    dayDifference = WorkedTotalDays(personId)

    totalDeservedRight = TotalDeservedRight(personId)
    totalApprovedRight = TotalApprovedRight(personId)
    totalAwatingApprovelRight = TotalAwatingApprovelRight(personId)

    result['TotalDeservedRight'] = totalDeservedRight
    result['TotalApprovedRight'] = totalApprovedRight
    result['TotalAwatingApprovelRight'] = totalAwatingApprovelRight
    result['BalanceRigth'] = totalDeservedRight - ( totalApprovedRight + totalAwatingApprovelRight )
    result['NumberOfDaysSubjestToRight'] = NumberOfDaysSubjestToRight(personId,dayDifference)
    result['NextRighNumberOfDaysSubjestToRighttTime'] = NextRighNumberOfDaysSubjestToRighttTime(personId,dayDifference)
    result['RightToBeDeserved'] = RightToBeDeserved(personId,dayDifference)

    return result

def TotalApprovedRight(personId):
    right  = Right.objects.filter(Person=personId,RightStatus=EnumRightStatus.Onaylandi,RightType= EnumRightTypes.Yillik)
    number = 0
    if  right:
        for r in right:
            number +=  r.RightNumber
    return number

def TotalAwatingApprovelRight(personId):
    right  = Right.objects.filter(Person=personId,RightStatus=EnumRightStatus.OnayBekliyor,RightType= EnumRightTypes.Yillik)
    number = 0
    if  right:
        for r in right:
            number +=  r.RightNumber
    return number


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