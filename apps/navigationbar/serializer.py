from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from .models import NavigationBar

class NavigationBarSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavigationBar
        fields = ('__all__')

class NavigationBarItemsSerializer(serializers.ModelSerializer):    
    items =serializers.SerializerMethodField()
    class Meta:
        model = NavigationBar
        fields = '__all__'

    def get_items(self,obj):
        if obj.any_children:
            return NavigationBarItemsSerializer(obj.children(), many=True).data
    


    


