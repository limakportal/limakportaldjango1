from rest_framework import serializers
from .models import Right
from apps.person.serializer import PersonSerializer
from apps.rightstatus.serializer import RightStatusSerializer
from apps.righttype.serializer import RightTypeSerializer
from apps.person.models import Person
from ..rightleave.models import RightLeave
from django.db.models import Sum
from ..utils.enums import EnumRightTypes, EnumRightStatus
from ..businessrules.views import mail_yolla

from .bussinessrules import PersonRightSummary


class RightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Right
        fields = ('__all__')


class RightWithApproverSerializer(serializers.ModelSerializer):
    Person = PersonSerializer()
    RightStatus = RightStatusSerializer()
    RightType = RightTypeSerializer()

    Approver1FullName = serializers.SerializerMethodField('apporover1_full_name')
    PersonFullName = serializers.SerializerMethodField('person_full_name')
    PersonApprover1 = serializers.SerializerMethodField()
    PersonRightSummary = serializers.SerializerMethodField()

    class Meta:
        model = Right
        fields = (
            'id',
            'EndDate',
            'StartDate',
            'DateOfReturn',
            'Telephone',
            'Approver1',
            'RightNumber',
            'DenyExplanation',
            'CreatedDate',
            'CreatedBy',
            'ModifiedDate',
            'ModifiedBy',
            'Person',
            'RightType',
            'RightStatus',
            'Approver1FullName',
            'PersonFullName',
            'PersonApprover1',
            'HrHasField',
            'RightPicture',
            'PersonRightSummary'
        )

    def apporover1_full_name(self, obj):
        if obj.Approver1 != None:
            try:
                personel = Person.objects.get(id=obj.Approver1)
                serializer = PersonSerializer(personel).data
                return serializer['Name'] + ' ' + serializer['Surname']
            except:
                return None
        return None

    def person_full_name(self, obj):
        try:
            person = Person.objects.get(id=obj.Person.id)
            serializer = PersonSerializer(person).data
            return serializer['Name'] + ' ' + serializer['Surname']
        except:
            return None

    def get_PersonApprover1(self, obj):
        if obj.Approver1 != None:
            try:
                person = Person.objects.get(id=obj.Approver1)
                serializer = PersonSerializer(person).data
                return serializer
            except:
                return None

    def get_PersonRightSummary(self, obj):
        try:
            result = PersonRightSummary(obj.Person_id)
            return result
        except:
            return None


class RightAllDetailsSerializer(serializers.ModelSerializer):
    RightAll = serializers.SerializerMethodField()
    TotalRightBalance = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = (
            'RightAll',
            'TotalRightBalance'
        )

    def get_RightAll(self, obj):

        rights = Right.objects.filter(Person_id=obj.id)
        serializer = RightSerializer(rights, many=True)
        return serializer.data

    def get_TotalRightBalance(self, obj):
        # totalleavebalance = GetRightBalance(obj.id)
        # return totalleavebalance

        rightleave = RightLeave.objects.filter(Person=obj.id)
        if rightleave:
            leave = rightleave.aggregate(total=Sum('Earning'))
            right = Right.objects.filter(Person=obj.id, RightStatus=EnumRightStatus.Onaylandi,
                                         RightType=EnumRightTypes.Yıllık)
            number = 0
            if right:
                for r in right:
                    number += r.RightNumber
            total = leave['total'] - number
        else:
            return 0
        return total


class RightAllDetailsSerializer2(serializers.ModelSerializer):
    TotalRightBalance = serializers.SerializerMethodField()

    class Meta:
        model = Right
        fields = (
            'id',
            'Person',
            'EndDate',
            'StartDate',
            'DateOfReturn',
            'Telephone',
            'Approver1',
            'RightType',
            'RightStatus',
            'RightNumber',
            'DenyExplanation',
            'HrHasField',
            'KvkkIsChecked',
            'RightPicture',
            'TotalRightBalance'
        )

    def get_TotalRightBalance(self, obj):
        # totalleavebalance = GetRightBalance(obj.id)
        # return totalleavebalance

        rightleave = RightLeave.objects.filter(Person=obj.Person_id)
        if rightleave:
            leave = rightleave.aggregate(total=Sum('Earning'))
            right = Right.objects.filter(Person=obj.id, RightStatus=EnumRightStatus.Onaylandi,
                                         RightType=EnumRightTypes.Yıllık)
            number = 0
            if right:
                for r in right:
                    number += r.RightNumber
            total = leave['total'] - number
        else:
            return 0
        return total


class TodayOnLeavePersonByPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            'id',
            'Name',
            'Surname',
            'Email'
        )
