from django.db import models
from apps.person.models import Person

class PersonBusiness(models.Model):
    class Meta:
        db_table = 'PersonBusiness'

    Person = models.ForeignKey(Person,on_delete=models.CASCADE)
    ContractType = models.IntegerField(blank=True,null=True)
    JobStartDate = models.DateField(blank=True, null=True)
    Degree = models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    JobCode = models.CharField(max_length = 100 , blank=True, null=True)

    def __str__(self):
        return self.Person.Name
