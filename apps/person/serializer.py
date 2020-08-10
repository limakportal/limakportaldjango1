from rest_framework import serializers
from .models import Person
from apps.gender.serializer import GenderSerializer
from apps.nationality.serializer import NationalitySerializer
from apps.city.serializer import CitySerializer
from apps.maritalstatus.serializer import MaritalStatusSerializer

class PersonSerializer(serializers.ModelSerializer):
    # Gender = GenderSerializer()
    # Nationality = NationalitySerializer()
    # RegisteredProvinceID = NationalitySerializer()
    # PlaceOfRegistryID = NationalitySerializer()
    # MaritalStatusID = NationalitySerializer()

    class Meta:
        model = Person
        fields = ('__all__')
        # fields = [
        #     'id',
        #     'Name',
        #     'Gender'
        # ]