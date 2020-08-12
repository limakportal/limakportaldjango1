from rest_framework import serializers
from .models import Right
from apps.person.serializer import PersonSerializer
from apps.rightstatus.serializer import RightStatusSerializer
from apps.righttype.serializer import RightTypeSerializer

class RightSerializer(serializers.ModelSerializer):
    Person = PersonSerializer()
    RightStatus = RightStatusSerializer()
    RightType = RightTypeSerializer()
    Approver1 = PersonSerializer()
    class Meta:
        model = Right
        fields = ('__all__')

class RightWithApproverSerializer(serializers.ModelSerializer):
    # Person = PersonSerializer()
    # RightStatus = RightStatusSerializer()
    # RightType = RightTypeSerializer()
    # Approver1 = PersonSerializer()
    class Meta:
        model = Right
        fields = ('__all__')
