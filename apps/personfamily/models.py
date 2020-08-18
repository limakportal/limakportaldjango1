from django.db import models
from apps.person.models import Person
from apps.gender.models import Gender

class PersonFamily(models.Model):
    class Meta:
        db_table =  'PersonFamily'

    Person = models.ForeignKey(Person,on_delete=models.CASCADE)
    Name = models.CharField(max_length = 100 , blank=True, null=True)
    Surname = models.CharField(max_length = 100 , blank=True, null=True)
    IdentityNumber = models.CharField(max_length = 20 , blank=True, null=True)
    Birtyday = models.DateTimeField(blank=True, null=True)
    Gender = models.ForeignKey(Gender,on_delete=models.CASCADE,blank=True, null=True)
    Telephone = models.CharField(max_length = 20 , blank=True, null=True)
    Relation = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.Person.Name


    
