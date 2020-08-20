from rest_framework import serializers
from .models import Staff

from rest_framework.serializers import ModelSerializer
from apps.title.serializer import TitleSerializer
from apps.role.serializer import RoleSerializer
from apps.organization.models import Organization


class OrganizationForStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = (
            'id',
            'Name'
        )


class StaffSerializer(serializers.ModelSerializer):
    Title = TitleSerializer()
    Role = RoleSerializer()
    Organization = OrganizationForStaffSerializer()
    class Meta:
        model = Staff
        fields = ('__all__')



