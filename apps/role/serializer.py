from rest_framework import serializers
from .models import Role

from ..authority.models import Authority
from ..authority.serializer import AuthoritySerializer

from ..permission.models import Permission
from ..permission.serializer import PermissionSerializer

class RoleSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Role
        fields = ('__all__')

class RoleViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = (
            'id',
            'Name',
            'Permissions'
        )
    Permissions = serializers.SerializerMethodField()
    def get_Permissions(self,obj):
        allPermission = []
        authoriyes = Authority.objects.filter(Role_id = obj.id)
        for authoriye in authoriyes:
            permissions = Permission.objects.filter(id = authoriye.Permission_id)
            for permission in permissions:
                allPermission.append(permission)
        return PermissionSerializer(allPermission,many=True).data


        






