from rest_framework import serializers
from .models import PersonFamily

class PersonFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonFamily
        fields = ('__all__')