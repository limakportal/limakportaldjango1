from rest_framework import serializers
from .models import Person
from apps.gender.serializer import GenderSerializer
from apps.nationality.serializer import NationalitySerializer
from apps.city.serializer import CitySerializer
from apps.maritalstatus.serializer import MaritalStatusSerializer

class PersonSerializer(serializers.ModelSerializer):
    Gender = GenderSerializer(read_only=True)
    Nationality = NationalitySerializer(read_only=True)
    RegisteredProvinceID = NationalitySerializer(read_only=True)
    PlaceOfRegistryID = NationalitySerializer(read_only=True)
    MaritalStatusID = NationalitySerializer(read_only=True)

    class Meta:
        model = Person
        fields = ('__all__')
        # fields = [
        #     'id',
        #     'Name',
        #     'Gender'
        # ]