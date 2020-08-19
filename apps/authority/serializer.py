from rest_framework import serializers
from .models import Permission
from .models import Role
from .models import Authority

from apps.permission.serializer import PermissionSerializer
from apps.role.serializer import RoleSerializer
from apps.permission.serializer import PermissionSerializer


class AuthoritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Authority
        Role = RoleSerializer()
        Permission = PermissionSerializer()  
        fields = ('__all__')





        



