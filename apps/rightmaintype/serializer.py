from rest_framework import serializers
from .models import RightMainType

class RightMainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RightMainType
        fields = ('__all__')
