from rest_framework import serializers

from ..organization.models import Organization
from ..organization.serializer import OrganizationSerializer


class OrganizationTreeByAccountId(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = (
            '__all__'
        )

    # Emrah = serializers.SerializerMethodField()

    # def get_Emrah(self,obj):
    #     organization = Organization.objects.all()
    #     serializers = OrganizationSerializer(organization,many=True)
    #     return serializers.data


