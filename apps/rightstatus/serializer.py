from rest_framework import serializers
from .models import RightStatus

class RightStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RightStatus
        fields = ('__all__')
