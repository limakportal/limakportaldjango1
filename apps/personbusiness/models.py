from django.db import models
from apps.person.models import Person

class PersonBusiness(models.Model):
    class Meta:
        db_table = 'PersonBusiness'

    Person = models.ForeignKey(Person,on_delete=models.CASCADE)
    ContractType = models.IntegerField(blank=True,null=True)
    JobStartDate = models.DateTimeField(blank=True, null=True)
    FirstBudget2 = models.DecimalField(max_digits=8, decimal_places=2,blank=True, null=True)
    JobCode = models.CharField(max_length = 100 , blank=True, null=True)
    RegisterNo = models.CharField(max_length=100,blank=True,null=True)
    SGKRegisterNo = models.CharField(max_length=100,blank=True,null=True)
    SGKEnterDate = models.DateTimeField(auto_now_add=True,max_length=50,blank=True,null=True)
    LeaveDate = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.Person.Name
