from rest_framework import serializers
from .models import Role

from ..authority.models import Authority
from ..permission.models import Permission
from ..userrole.models import UserRole
from ..account.models import Account
from ..person.models import Person

from ..authority.serializer import AuthoritySerializer
from ..permission.serializer import PermissionSerializer



class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person       
        fields = ('__all__')

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
             

class RoleViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = (
            'id',
            'Name',
            'IsHierarchical',
            'Permissions',
            'Users'
        )
    Permissions = serializers.SerializerMethodField()
    Users = serializers.SerializerMethodField()

    def get_Permissions(self,obj):
        allPermission = []
        authoriyes = Authority.objects.filter(Role_id = obj.id)
        for authoriye in authoriyes:
            permissions = Permission.objects.filter(id = authoriye.Permission_id)
            for permission in permissions:
                allPermission.append(permission)
        return PermissionSerializer(allPermission,many=True).data

    def get_Users(self,obj):
        allAccounts = [] 
        userRoles = UserRole.objects.filter(Role_id = obj.id)
        for userrole in userRoles:
            account = Account.objects.filter(id = userrole.Account_id)
            for user in account:
                allAccounts.append(user)
        return AccountsDetailSerializer(allAccounts,many=True).data







        






