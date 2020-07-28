from rest_framework import serializers
from .models import PersonHistory

class PersonHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonHistory
        fields = ('__all__')