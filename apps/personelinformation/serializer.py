from rest_framework import serializers
from .models import PersonelInformation

class PersonelInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonelInformation
        fields = ('__all__')
