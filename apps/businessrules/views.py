from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from django.core.mail import send_mail

from ..organization.models import Organization
from ..organization.serializer import OrganizationSerializer ,OrganizationTreeSerializer
from ..businessrules.serializer import (OrganizationTreeByAccountId)

class PersonList(APIView):
    def get(self,request):
        response = {}

        try:
            organizationObj = Organization.objects.get(id = 20)
            serializer = OrganizationWithPersonTree(organizationObj)
            response['Menu'] = serializer.data
        except :
            response['Menu'] = None

        return Response(response,status=status.HTTP_200_OK)

class OrganizationWithPersonTree(serializers.ModelSerializer):
    ChildOrganization = SerializerMethodField()
    class Meta:
        model = Organization
        fields = (
            'id',
            'Name',
            'ChildOrganization'
            )
    def get_ChildOrganization(self, obj):
        if obj.any_children:
            return OrganizationWithPersonTree(obj.children(), many=True).data


def mail_yolla(baslik,icerik,to,send):
    # baslik = 'İzin Kullanım Hakkında'
    # icerik = 'Ayça Bilmez’in ... tarihine kadar ... gün iznini kullanması gerekmektedir. Lütfen çalışanınızı mevcut iznini kullanmaya yönlendiriniz.'
    send_mail(baslik, icerik, to, send, fail_silently=False)