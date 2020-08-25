from rest_framework import serializers
from .models import Staff

from rest_framework.serializers import ModelSerializer
from apps.title.serializer import TitleSerializer
from apps.role.serializer import RoleSerializer
from apps.organization.models import Organization

from ..title.models import Title
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
    class Meta:
        model = Staff
        fields = (
            'id',
            'Organization',
            'Person',
            'Title',
            'Role',
            'PersonObj',
            'TitleObj',
            'OrganizationObj'
        )
    OrganizationObj = serializers.SerializerMethodField()
    PersonObj = serializers.SerializerMethodField()
    TitleObj = serializers.SerializerMethodField()

    def get_PersonObj(self,obj):
        try:
            person = Person.objects.get(id=obj.Person_id)
            serializer = PersonSerializer(person)
            return serializer.data
        except :
            return None

    def get_TitleObj(self,obj):
        try:
            title = Title.objects.get(id=obj.Title_id)
            serializer = TitleSerializer(title)
            return serializer.data
        except :
            return None

    def get_OrganizationObj(self,obj):
        try:
            organization = Organization.objects.get(id=obj.Organization_id)
            serializer = TitleSerializer(organization)
            return serializer.data
        except :
            return None

class StafForPersonSerializer(serializers.ModelSerializer):
    Title = TitleSerializer()
    Role = RoleSerializer()
    Organization = OrganizationForStaffSerializer()
    class Meta:
        model = Staff
        fields = ('__all__')



