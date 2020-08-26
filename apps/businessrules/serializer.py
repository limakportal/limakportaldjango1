from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from ..organization.models import Organization
from ..staff.models import Staff
from ..person.models import Person

from ..organization.serializer import OrganizationSerializer
from ..person.serializer import PersonSerializer 




class OrganizationTreeByAccountId(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = (
            '__all__'
        )



class OrganizationWithPersonTreeSerializer(serializers.ModelSerializer):
    ChildOrganization = SerializerMethodField()
    class Meta:
        model = Organization
        fields = (
            'id',
            'Name',
            'ChildOrganization'
            )
    def get_ChildOrganization(self, obj):
        if obj.any_children:
            return OrganizationWithPersonTreeSerializer(obj.children(), many=True).data

            
             