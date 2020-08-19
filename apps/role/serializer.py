from rest_framework import serializers
from .models import Role

class RoleSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Role
        fields = ('__all__')