from rest_framework import serializers
from .models import Person
from apps.gender.serializer import GenderSerializer
from apps.nationality.serializer import NationalitySerializer
from apps.city.serializer import CitySerializer
from apps.maritalstatus.serializer import MaritalStatusSerializer
from apps.personelinformation.serializer import PersonelInformationSerializer
from apps.personelinformation.models import PersonelInformation
from apps.personidentity.models import PersonIdentity
from apps.personidentity.serializer import PersonIdentitySerializer
from apps.personbusiness.models import PersonBusiness
from apps.personbusiness.serializer import PersonBusinessSerializer
from apps.personeducation.models import PersonEducation
from apps.personeducation.serializer import PersonEducationSerializer
from apps.personfamily.models import PersonFamily
from apps.personfamily.serializer import PersonFamilySerializer

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person       
        fields = ('__all__')


class PersonViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person        
        fields = (
            'id',
            'Name',
            'Surname',
            'IdentityID',
            'Address',
            'Telephone',
            'State',
            'IdentitySerialNumber',
            'IdentityVolumeNo',
            'Email',
            'Picture',
            'Nationality',
            'PlaceOfRegistryID',
            'PersonelInformation',
            'PersonIdentity',
            'PersonBusiness',
            'PersonEducation',
            'PersonFamily'
        )

    # Id = serializers.CharField(source='id')
    # NationalityId = serializers.CharField(source='Nationality')

    PersonelInformation = serializers.SerializerMethodField()
    PersonIdentity = serializers.SerializerMethodField()
    PersonBusiness = serializers.SerializerMethodField()
    PersonEducation = serializers.SerializerMethodField()
    PersonFamily = serializers.SerializerMethodField()
    
    def get_PersonelInformation(self, obj):
        try:
            personInformation = PersonelInformation.objects.get(Person=obj.id)
            serializer = PersonelInformationSerializer(personInformation)
            return serializer.data
        except:
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



        



