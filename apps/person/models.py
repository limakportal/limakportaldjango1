from django.db import models

from apps.gender.models import Gender
from apps.maritalstatus.models import MaritalStatus
from apps.nationality.models import Nationality

import base64


class Person(models.Model):
    class Meta:
        db_table = 'Person'

    Name = models.CharField(max_length=50,blank=True,null=True)
    Surname = models.CharField(max_length=50,blank=True,null=True)
    IdentityID = models.CharField(max_length=50,blank=True,null=True)
    Nationality = models.ForeignKey(Nationality,on_delete=models.CASCADE,related_name='NationalityId',blank=True, null=True)
    Address = models.CharField(max_length=200,blank=True,null=True)
    Telephone = models.CharField(max_length=50,blank=True,null=True)
    State = models.IntegerField(blank=True,null=True)
    Email = models.CharField(max_length=50,blank=True,null=True)
    Picture = models.BinaryField(blank=True,null=True)
    PictureTypes = models.CharField(max_length=50, blank=True, null=True)

    @property
    def PictureData(self):
        return f"data:{self.PictureTypes};base64,{base64.b64encode(self.Picture).decode('utf-8')}"


    def __str__(self):
        return self.Name




