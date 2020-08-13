from rest_framework import serializers
from .models import Person
from apps.gender.serializer import GenderSerializer
from apps.nationality.serializer import NationalitySerializer
from apps.city.serializer import CitySerializer
from apps.maritalstatus.serializer import MaritalStatusSerializer
from apps.personelinformation.serializer import PersonelInformationSerializer
from apps.personelinformation.models import PersonelInformation

class PersonSerializer(serializers.ModelSerializer):
    # Id = serializers.CharField(source='id')
    # NationalityId = serializers.CharField( read_only=True,source='Nationality')

    class Meta:
        model = Person
        
        fields = ('__all__')
        # fields = (
        #     'Id',
        #     'Name',
        #     'Surname',
        #     'IdentityID',
        #     'Address',
        #     'Telephone',
        #     # 'BirthDate',
        #     'State',
        #     'IdentitySerialNumber',
        #     'IdentityVolumeNo',
        #     # 'MothersName',
        #     # 'FathersName',
        #     # 'BloodType',
        #     'Email',
        #     'Picture',
        #     'NationalityId',
        #     # 'Gender',
        #     # 'MaritalStatusID',
        #     # 'RegisteredProvinceID',
        #     'PlaceOfRegistryID'
        # )

class PersonViewSerializer(serializers.ModelSerializer):

    Id = serializers.CharField(source='id')
    NationalityId = serializers.CharField(source='Nationality')

    PersonelInformation = serializers.SerializerMethodField()
    
    def get_PersonelInformation(self, person):       
        return PersonelInformationSerializer(PersonelInformation.objects.get(Person=person.id)).data

   

    class Meta:
        model = Person        
        fields = (
            'Id',
            'Name',
            'Surname',
            'IdentityID',
            'Address',
            'Telephone',
            # 'BirthDate',
            'State',
            'IdentitySerialNumber',
            'IdentityVolumeNo',
            # 'MothersName',
            # 'FathersName',
            # 'BloodType',
            'Email',
            'Picture',
            'NationalityId',
            # 'Gender',
            # 'MaritalStatusID',
            # 'RegisteredProvinceID',
            'PlaceOfRegistryID',
            'PersonelInformation'
        )

