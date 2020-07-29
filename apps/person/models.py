from django.db import models
from apps.gender.models import Gender
from apps.maritalstatus.models import MaritalStatus
from apps.city.models import City
from apps.nationality.models import Nationality

# Create your models here.


class Person(models.Model):
    class Meta:
        db_table = 'Person'

    Name = models.CharField(max_length=50,blank=True,null=True)
    Surname = models.CharField(max_length=50,blank=True,null=True)
    IdentityID = models.CharField(max_length=50,blank=True,null=True)
    Nationality = models.ForeignKey(Nationality,on_delete=models.CASCADE)
    Address = models.CharField(max_length=50,blank=True,null=True)
    Telephone = models.CharField(max_length=50,blank=True,null=True)
    BirthDate = models.DateField(max_length=50,blank=True,null=True)
    State = models.IntegerField(blank=True,null=True)
    Gender = models.ForeignKey(Gender,on_delete=models.CASCADE)
    MaritalStatusID = models.ForeignKey(MaritalStatus,on_delete=models.CASCADE)
    RegisteredProvinceID = models.ForeignKey(City,on_delete=models.CASCADE,related_name='RegisteredProvinceID')
    PlaceOfRegistryID = models.ForeignKey(City,on_delete=models.CASCADE,related_name='PlaceOfRegistryID')
    IdentitySerialNumber = models.CharField(max_length=50,blank=True,null=True)
    IdentityVolumeNo = models.CharField(max_length=50,blank=True,null=True)
    MothersName = models.CharField(max_length=50,blank=True,null=True)
    FathersName = models.CharField(max_length=50,blank=True,null=True)
    BloodType = models.CharField(max_length=50,blank=True,null=True)
    Email = models.CharField(max_length=50,blank=True,null=True)
    Picture = models.BinaryField(max_length=(1<<24)-1)

    # def __str__(self):
    #     return self.Name




