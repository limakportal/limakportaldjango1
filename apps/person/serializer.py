from rest_framework import serializers
from .models import Personel

class PersonelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personel
        fields = ('__all__')
        # fields = [
        #     'id',
        #     'Name',
        #     'Surname',
        #     'Citizenship'
        # ]