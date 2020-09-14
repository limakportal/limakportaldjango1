from rest_framework import serializers
from .models import PersonEmployment

class PersonEmploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonEmployment
        fields = ('__all__')
