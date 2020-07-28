from django.db import models
from apps.person.models import Person

# Create your models here.


class PersonelInformation(models.Model):
    class Meta:
        db_table = 'PersonelInformation'

    Person = models.ForeignKey(Person,on_delete=models.CASCADE)
    RegisterNo = models.CharField(max_length=100,blank=True,null=True)
    SGKRegisterNo = models.CharField(max_length=100,blank=True,null=True)
    SGKEnterDate = models.DateField(auto_now_add=True,max_length=50,blank=True,null=True)
    LimakEnterDate = models.DateField(auto_now_add=True,max_length=50,blank=True,null=True)

