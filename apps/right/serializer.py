from rest_framework import serializers
from .models import Right

class RightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Right
        fields = ('__all__')
