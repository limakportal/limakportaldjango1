from django.db import models
from apps.person.models import Person

class PersonBusiness(models.Model):
    class Meta:
        db_table = 'PersonBusiness'

    Person = models.ForeignKey(Person,on_delete=models.CASCADE)
    ContractType = models.IntegerField(blank=True,null=True)
    JobStartDate = models.DateField()
    FirstBudget = models.DecimalField(max_digits=20, decimal_places=2)
    JobCode = models.CharField(max_length = 100 , blank=True, null=True)
    RegisterNo = models.CharField(max_length=100,blank=True,null=True)
    SGKRegisterNo = models.CharField(max_length=100,blank=True,null=True)
    SGKEnterDate = models.DateField(auto_now_add=True,max_length=50,blank=True,null=True)

    def __str__(self):
        return self.Person.Name
