from rest_framework import serializers
from .models import District

classDistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ('__all__')
