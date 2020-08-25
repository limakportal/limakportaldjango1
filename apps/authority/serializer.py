from rest_framework import serializers
from .models import Authority

from apps.permission.serializer import PermissionSerializer
from apps.role.serializer import RoleSerializer



class AuthoritySerializer(serializers.ModelSerializer):
    # Role = RoleSerializer()
    # Permission = PermissionSerializer()
    class Meta:
        model = Authority  
        fields = ('__all__')





        



