from django.db import models
from apps.person.models import Person

# Create your models here.


class PersonHistory(models.Model):
    class Meta:
        db_table = 'PersonHistory'

    Person = models.ForeignKey(Person,on_delete=models.CASCADE)
    StaffID = models.IntegerField(blank=True,null=True)
    EntryDate = models.DateField(auto_now_add=True,max_length=50,blank=True,null=True)
    TerminationDate = models.DateField(auto_now_add=True,max_length=50,blank=True,null=True)




