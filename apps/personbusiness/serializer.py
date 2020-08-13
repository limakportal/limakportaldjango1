from rest_framework import serializers
from .models import PersonBusiness

class PersonBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonBusiness
        fields =('__all__')