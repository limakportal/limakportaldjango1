from rest_framework import serializers
from .models import Staff

from rest_framework.serializers import ModelSerializer
from apps.title.serializer import TitleSerializer
from apps.role.serializer import RoleSerializer
from apps.organization.models import Organization


from ..title.serializer import TitleSerializer
from ..person.models import Person
from ..organization.models import Organization



class OrganizationForStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = (
            'id',
            'Name'
        )


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ('__all__')

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person       
        fields = ('__all__')
class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('__all__')

class StaffJoinSerializer(serializers.ModelSerializer):
    Organization = OrganizationSerializer()
    Person = PersonSerializer()
    Title = TitleSerializer()
    class Meta:
        model = Staff
        fields = ('__all__')

class StafForPersonSerializer(serializers.ModelSerializer):
    Title = TitleSerializer()
    Role = RoleSerializer()
    Organization = OrganizationForStaffSerializer()
    class Meta:
        model = Staff
        fields = ('__all__')



