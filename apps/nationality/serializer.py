from rest_framework import serializers
from .models import Nationality

class NationalitySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Nationality
        fields = ('__all__')
