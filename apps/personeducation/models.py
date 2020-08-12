from django.db import models
from apps.person.models import Person
from apps.city.models import City

class PersonEducation(models.Model):
    class Meta:
        db_table = 'PersonEducation'

    PersonId = models.ForeignKey(Person,on_delete=models.CASCADE)
    SchoolName = models.CharField(max_lenght = 100 , blank=True, null=True)
    SchoolTypeId = models.IntegerField(blank=True,null=True)
    StartDate = models.DateField(blank=True, null=True)
    GraduationDate = models.DateField(blank=True, null=True)
    CityId = models.ForeignKey(City,on_delete=models.CASCADE,blank=True, null=True)
    Description = models.CharField(max_lenght = 200 ,blank=True, null=True)
    Degree = models.DecimalField(max_digits=None,decimal_places=None,blank=True, null=True)
    Faculty = models.CharField(max_lenght = 100,blank=True, null=True)
    Section = models.CharField(max_lenght= 100,blank=True, null=True)
    ForeignLanguage = models.CharField(max_lenght = 200,blank=True, null=True)
    Section = models.BinaryField(blank=True, null=True)