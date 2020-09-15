from rest_framework import serializers

from ..organization.models import Organization
from ..organizationtype.models import OrganizationType
from ..staff.models import Staff


class GetPersonCountWithOrganizationSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField()
    organizationtype = serializers.SerializerMethodField()
    personcount = serializers.SerializerMethodField()
    UpperOrganization = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = (
            'organization',
            'organizationtype',
            'personcount',
            'UpperOrganization'
        )

    def get_organization(self, obj):
        try:
            organization = Organization.objects.get(id=obj.id)
            return organization.Name
        except:
            return None

    def get_organizationtype(self, obj):
        try:
            organizationtype = OrganizationType.objects.get(id=obj.OrganizationType_id)
            return organizationtype.Name
        except:
            return None

    def get_personcount(self, obj):
        try:
            staff = Staff.objects.filter(Organization_id=obj.id)
            return len(staff)
        except:
            return 0

    def get_UpperOrganization(self, obj):
        try:
            organization = Organization.objects.get(id=obj.id)
            return organization.OrganizationType_id
        except:
            return None


class GetAllOrganizationtypeId2WithTotalStaffSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField()
    personcount = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = (
            'organization',
            'personcount'
        )

    def get_organization(self, obj):
        try:
            organization = Organization.objects.get(id=obj.id)
            return organization.Name
        except:
            return None

    def get_personcount(self, obj):
        try:
            staff = Staff.objects.filter(Organization_id=obj.id)
            return len(staff)
        except:
            return 0
