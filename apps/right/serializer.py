from rest_framework import serializers
from .models import Right
from apps.person.serializer import PersonSerializer
from apps.rightstatus.serializer import RightStatusSerializer
from apps.righttype.serializer import RightTypeSerializer
from apps.person.models import Person

class RightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Right
        fields = ('__all__')

class RightWithApproverSerializer(serializers.ModelSerializer):
    Person = PersonSerializer()
    RightStatus = RightStatusSerializer()
    RightType = RightTypeSerializer()

    Approver1FullName = serializers.SerializerMethodField('apporover1_full_name')
    Approver2FullName = serializers.SerializerMethodField('apporover2_full_name')
    PersonFullName = serializers.SerializerMethodField('person_full_name')
    PersonApprover1 = serializers.SerializerMethodField()
    PersonApprover2 = serializers.SerializerMethodField()

    def apporover1_full_name(self,obj):
        if obj.Approver1 != None:
            personel = Person.objects.get(id=obj.Approver1)
            serializer = PersonSerializer(personel).data
            return serializer['Name'] + ' ' + serializer['Surname']
        return None

    def apporover2_full_name(self,obj):
        if obj.Approver1 != None:
            personel = Person.objects.get(id=obj.Approver2)
            serializer = PersonSerializer(personel).data
            return serializer['Name'] + ' ' + serializer['Surname']
        return None

    def person_full_name(self,obj):
        person = Person.objects.get(id=obj.Person.id)
        serializer = PersonSerializer(person).data
        return serializer['Name'] + ' ' +serializer['Surname']

    def get_PersonApprover1(self,obj):
        if obj.Approver1 != None:
            person = Person.objects.get(id = obj.Approver1)
            serializer = PersonSerializer(person).data
            return serializer

    def get_PersonApprover2(self,obj):
        if obj.Approver1 != None:
            person = Person.objects.get(id = obj.Approver2)
            serializer = PersonSerializer(person).data
            return serializer

    class Meta:
        model = Right
        fields = (
            'id',
            'EndDate',
            'DateOfReturn',
            'Address',
            'Telephone',
            'Approver1',
            'Approver2',
            'RightNumber',
            'DenyExplanation',
            'Person',
            'RightType',
            'RightStatus',
            'Approver1FullName',
            'Approver2FullName',
            'PersonFullName',
            'PersonApprover1',
            'PersonApprover2'
        )
