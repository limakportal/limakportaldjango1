from django.db import models
from apps.person.models import Person

class RightLeave(models.Model):
    class Meta:
        db_table = 'RightLeave'

    Earning = models.IntegerField(blank=True, null=True)
    Year = models.IntegerField(blank=True, null=True)
    Person = models.ForeignKey(Person,on_delete = models.CASCADE)
    Optime = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.Person.Name