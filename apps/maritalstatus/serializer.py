from rest_framework import serializers
from .models import MaritalStatus

class MaritalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaritalStatus
        fields = ('__all__')
