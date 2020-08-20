from rest_framework import serializers
from .models import RightLeave

class RightLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = RightLeave
        fields = ('__all__')
