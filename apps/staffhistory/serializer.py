from rest_framework import serializers

from .models import StaffHistory


class StaffHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffHistory
        fields = '__all__'
