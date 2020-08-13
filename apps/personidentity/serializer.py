from rest_framework import serializers
from .models import PersonIdentity


class PersonIdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonIdentity
        fields = ('__all__')