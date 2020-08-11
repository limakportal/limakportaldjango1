from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from .models import Organization
from apps.organizationtype.serializer import OrganizationTypeSerializer
from apps.status.serializer import StatusSerializer

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('__all__')

class OrganizationTreeSerializer(serializers.ModelSerializer):
    Organization = SerializerMethodField()
    Status = StatusSerializer()
    OrganizationType = OrganizationTypeSerializer()
    UpperOrganization = OrganizationSerializer()


    class Meta:
        model = Organization
        fields = ('__all__')

    def get_Organization(self, obj):
        if obj.any_children:
            return OrganizationTreeSerializer(obj.children(), many=True).data



    


