from rest_framework import serializers
from .models import VocationDays


class VocationDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = VocationDays
        fields = ('__all__')

