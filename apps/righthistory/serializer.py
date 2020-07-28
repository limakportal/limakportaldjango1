from rest_framework import serializers
from .models import RightHistory

class RightHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RightHistory
        fields = ('__all__')
