from django.db import models
from apps.person.models import Person
from apps.staff.models import Staff

# Create your models here.


class PersonHistory(models.Model):
    class Meta:
        db_table = 'PersonHistory'

    Person = models.ForeignKey(Person,on_delete=models.CASCADE)
    Staff = models.ForeignKey(Staff,on_delete=models.CASCADE)
    EntryDate = models.DateField(auto_now_add=True,max_length=50,blank=True,null=True)
    TerminationDate = models.DateField(auto_now_add=True,max_length=50,blank=True,null=True)




