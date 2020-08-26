from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from ..organization.models import Organization
from ..staff.models import Staff
from ..person.models import Person
from apps.account.models import Account

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


class AccountsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'id',
            'email',
            'PersonId',
            'PersonName',
            'PersonSurname'
        )
    PersonId = serializers.SerializerMethodField()
    PersonName = serializers.SerializerMethodField()
    PersonSurname = serializers.SerializerMethodField()

    def get_PersonId(self,obj):
        try:
            person = Person.objects.get(Email = obj.email)
            serializer = PersonSerializer(person)
            return serializer.data['id']
        except :
            return None

    def get_PersonName(self,obj):
        try:
            person = Person.objects.get(Email = obj.email)
            serializer = PersonSerializer(person)
            return serializer.data['Name']
        except :
            return None

    def get_PersonSurname(self,obj):
        try:
            person = Person.objects.get(Email = obj.email)
            serializer = PersonSerializer(person)
            return serializer.data['Surname']
        except :
            return None
             