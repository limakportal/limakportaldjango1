from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from .models import NavigationBar

class NavigationBarSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavigationBar
        fields = ('__all__')