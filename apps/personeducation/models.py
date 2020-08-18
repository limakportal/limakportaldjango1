from django.db import models
from apps.person.models import Person
from apps.city.models import City

class PersonEducation(models.Model):
    class Meta:
        db_table = 'PersonEducation'

    Person = models.ForeignKey(Person,on_delete=models.CASCADE)
    SchoolName = models.CharField(max_length = 100 , blank=True, null=True)
    SchoolTypeId = models.IntegerField(blank=True,null=True)
    StartDate = models.DateTimeField(blank=True, null=True)
    GraduationDate = models.DateTimeField(blank=True, null=True)
    City = models.ForeignKey(City,on_delete=models.CASCADE,blank=True, null=True)
    Description = models.CharField(max_length = 200 ,blank=True, null=True)
    Degree = models.DecimalField(max_digits=5,decimal_places=2,blank=True, null=True)
    Faculty = models.CharField(max_length = 100,blank=True, null=True)
    Section = models.CharField(max_length= 100,blank=True, null=True)
    ForeignLanguage = models.CharField(max_length = 200,blank=True, null=True)
    Section = models.BinaryField(blank=True, null=True)

    def __str__(self):
        return self.Person.Name