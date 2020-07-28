from rest_framework import serializers
from .models import RightType

class RightTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RightType
        fields = ('__all__')
