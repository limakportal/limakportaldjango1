from django.db import models
from apps.person.models import Person
from apps.gender.models import Gender
from apps.maritalstatus.models import MaritalStatus
from apps.city.models import City
from apps.district.models import District

class PersonIdentity(models.Model):
    class Meta:
        db_table = 'PersonIdentity'
    
    Person = models.ForeignKey(Person,on_delete=models.CASCADE)
    SerialNumber = models.CharField(max_length = 100 , blank=True, null=True)
    FatherName = models.CharField(max_length = 100 , blank=True, null=True)
    MotherName = models.CharField(max_length = 100 , blank=True, null=True)
    PlaceOfBirthCity = models.ForeignKey(City,on_delete=models.CASCADE,related_name='PlaceOfBirthCity')
    PlaceOfBirthDistrict = models.ForeignKey(District,on_delete=models.CASCADE,related_name='PlaceOfBirthDistrict')
    RegisteredCity = models.ForeignKey(City,on_delete=models.CASCADE,related_name='RegisteredCity')
    RegisteredDistrict = models.ForeignKey(District,on_delete=models.CASCADE,related_name='RegisteredDistrict')
    BirthDate = models.DateField(blank=True, null=True)
    Gender = models.ForeignKey(Gender,on_delete=models.CASCADE,blank=True, null=True)
    MaritalStatus = models.ForeignKey(MaritalStatus,on_delete=models.CASCADE,blank=True, null=True)
    BloodType = models.CharField(max_length=50,blank=True,null=True)
    MilitaryStatus = models.IntegerField(blank=True,null=True)
    MilitaryDischargeData = models.DateField(blank=True, null=True)
    PreviousLastname = models.CharField(max_length = 100 , blank=True, null=True)

    def __str__(self):
        return self.Person.Name

    
