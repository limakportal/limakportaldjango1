from rest_framework import serializers
from .models import Person

from apps.gender.serializer import GenderSerializer
from apps.nationality.serializer import NationalitySerializer
from apps.city.serializer import CitySerializer
from apps.maritalstatus.serializer import MaritalStatusSerializer
from apps.personidentity.models import PersonIdentity
from apps.personidentity.serializer import PersonIdentitySerializer
from apps.personbusiness.models import PersonBusiness
from apps.personbusiness.serializer import PersonBusinessSerializer ,PersonBusinessForPersonListSerializer
from apps.personeducation.models import PersonEducation
from apps.personeducation.serializer import PersonEducationSerializer
from apps.personfamily.models import PersonFamily
from apps.personfamily.serializer import PersonFamilySerializer
from apps.staff.models import Staff
from apps.staff.serializer import StaffSerializer

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person       
        fields = ('__all__')

class PersonForListViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            'id',
            'Name',
            'Surname',
            'IdentityID',
            'Telephone',
            'Email'
        )


class PersonViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            'Person',
            'PersonBusiness',
            'Staff'
        )
    
    Person = serializers.SerializerMethodField()
    PersonBusiness = serializers.SerializerMethodField()
    Staff = serializers.SerializerMethodField()

    def get_Person(self,obj):
        try:
            person = Person.objects.get(id=obj.id)
            serializer = PersonForListViewSerializer(person)
            return serializer.data
        except expression as identifier:
            return None

    def get_PersonBusiness(self,obj):
        try:
            personBusiness = PersonBusiness.objects.get(Person = obj.id)
            serializer = PersonBusinessForPersonListSerializer(personBusiness)
            return serializer.data
        except:
            return None

    def get_Staff(self,obj):
        try:
            staff = Staff.objects.get(Person = obj.id)
            serializers = StaffSerializer(staff)
            return serializers.data
        except:
            return None



class PersonViewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person        
        fields = (
            'Person',
            'PersonIdentity',
            'PersonBusiness',
            'PersonEducation',
            'PersonFamily'
        )

    # Id = serializers.CharField(source='id')
    # NationalityId = serializers.CharField(source='Nationality')

    Person = serializers.SerializerMethodField()
    PersonIdentity = serializers.SerializerMethodField()
    PersonBusiness = serializers.SerializerMethodField()
    PersonEducation = serializers.SerializerMethodField()
    PersonFamily = serializers.SerializerMethodField()

    def get_Person(self,obj):
        try:
            person = Person.objects.get(id=obj.id)
            serializer = PersonSerializer(person)
            return serializer.data
        except expression as identifier:
            return None
    
    def get_PersonIdentity(self,obj):
        try:
            personIdentity = PersonIdentity.objects.get(Person=obj.id)
            serializer = PersonIdentitySerializer(personIdentity)
            return serializer.data
        except:
            return None

    def get_PersonBusiness(self,obj):
        try:
            personBusiness = PersonBusiness.objects.get(Person = obj.id)
            serializer = PersonBusinessSerializer(personBusiness)
            return serializer.data
        except:
            return None

    def get_PersonEducation(self,obj):
        personEducations = PersonEducation.objects.filter(Person = obj.id)
        serializer = PersonEducationSerializer(personEducations,many=True)
        return serializer.data

    def get_PersonFamily(self,obj):
        personFamilys = PersonFamily.objects.filter(Person = obj.id)
        serializer = PersonFamilySerializer(personFamilys , many = True)
        return serializer.data



        



