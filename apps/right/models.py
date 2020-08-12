from django.db import models
from apps.person.models import Person
from apps.righttype.models import RightType
from apps.rightstatus.models import RightStatus


class Right(models.Model):

    class Meta:
        db_table = 'Right'

    Person = models.ForeignKey(Person,on_delete = models.CASCADE)
    EndDate = models.DateField(auto_now_add=True,max_length=50,blank=True,null=True)
    DateOfReturn = models.DateField(auto_now_add=True,max_length=50,blank=True,null=True)
    Address = models.CharField(max_length=50,blank=True,null=True)
    Telephone = models.CharField(max_length=50,blank=True,null=True)
    Approver1 = models.IntegerField(blank=True,null=True)
    Approver2 = models.IntegerField(blank=True,null=True)
    RightType = models.ForeignKey(RightType,on_delete = models.CASCADE)
    RightStatus = models.ForeignKey(RightStatus, on_delete = models.CASCADE)
    RightNumber = models.IntegerField(blank=True,null=True)
    DenyExplanation = models.CharField(max_length=50,blank=True)