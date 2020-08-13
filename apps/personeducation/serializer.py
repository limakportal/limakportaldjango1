from rest_framework import serializers
from apps.personeducation.models import PersonEducation


class PersonEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonEducation
        fields = ('__all__')