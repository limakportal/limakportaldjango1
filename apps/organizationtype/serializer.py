from rest_framework import serializers
from .models import OrganizationType

class OrganizationTypeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = OrganizationType
        fields = ('__all__')
