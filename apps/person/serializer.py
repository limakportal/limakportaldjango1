from rest_framework import serializers
from .models import Person
from apps.gender.serializer import GenderSerializer
from apps.nationality.serializer import NationalitySerializer
from apps.city.serializer import CitySerializer
from apps.maritalstatus.serializer import MaritalStatusSerializer
from apps.personelinformation.serializer import PersonelInformationSerializer
from apps.personelinformation.models import PersonelInformation

class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('__all__')

class PersonViewSerializer(serializers.ModelSerializer):
    
    PersonelInformation = serializers.SerializerMethodField()
    
    def get_PersonelInformation(self, person):       
        return PersonelInformationSerializer(PersonelInformation.objects.get(Person=person.id)).data

    class Meta:
        model = Person        
        fields = (
            'id',
            'Name',
            'Surname',
            'IdentityID',
            'Address',
            'Telephone',
            'BirthDate',
            'State',
            'IdentitySerialNumber',
            'IdentityVolumeNo',
            'MothersName',
            'FathersName',
            'BloodType',
            'Email',
            'Picture',
            'Nationality',
            'Gender',
            'MaritalStatusID',
            'RegisteredProvinceID',
            'PlaceOfRegistryID',
            'PersonelInformation'
        )

