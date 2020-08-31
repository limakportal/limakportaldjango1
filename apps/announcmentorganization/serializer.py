from rest_framework import serializers
from .models import AnnouncmentOrganization

class AnnouncmentOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncmentOrganization
        fields = ('__all__')