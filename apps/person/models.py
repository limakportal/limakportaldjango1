from django.db import models
from apps.gender.models import Gender

# Create your models here.


class Person(models.Model):
    class Meta:
        db_table = 'Person'

    Name = models.CharField(max_length=50,blank=True,null=True)
    Surname = models.CharField(max_length=50,blank=True,null=True)
    IdentityID = models.CharField(max_length=50,blank=True,null=True)
    NationalityID = models.IntegerField(blank=True,null=True)
    Address = models.CharField(max_length=50,blank=True,null=True)
    Telephone = models.CharField(max_length=50,blank=True,null=True)
    BirthDate = models.DateField(max_length=50,blank=True,null=True)
    State = models.IntegerField(blank=True,null=True)
    Gender = models.ForeignKey(Gender,on_delete=models.CASCADE)
    MaritalStatusID = models.IntegerField(blank=True,null=True)
    RegisteredProvinceID = models.IntegerField(blank=True,null=True)
    PlaceOfRegistryID = models.IntegerField(blank=True,null=True)
    IdentitySerialNumber = models.CharField(max_length=50,blank=True,null=True)
    IdentityVolumeNo = models.CharField(max_length=50,blank=True,null=True)
    MothersName = models.CharField(max_length=50,blank=True,null=True)
    FathersName = models.CharField(max_length=50,blank=True,null=True)
    BloodType = models.CharField(max_length=50,blank=True,null=True)
    Email = models.CharField(max_length=50,blank=True,null=True)
    Picture = models.BinaryField(max_length=(1<<24)-1)

    # def __str__(self):
    #     return self.Name




