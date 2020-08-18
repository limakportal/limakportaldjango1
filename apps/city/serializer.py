from rest_framework import serializers
from .models import City

from apps.district.models import District
from apps.district.serializer import DistrictSerializer

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('__all__')

class CityViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            'id',
            'Name',
            'PlateCode',
            'Status',
            'District'
        )

    District = serializers.SerializerMethodField()
    def get_District(self,obj):
        district = District.objects.filter(City = obj.id).order_by('Name')
        serializer = DistrictSerializer(district , many = True)
        return serializer.data