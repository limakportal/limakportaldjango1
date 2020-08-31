from rest_framework import serializers
from .models import Announcment

class AnnouncmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcment
        fields = ('__all__')