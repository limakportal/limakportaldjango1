from django.db import models
from apps.person.models import Person


class User(models.Model):
    class Meta:
        db_table = 'User'

    Email = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    IsApproved = models.IntegerField(blank=True,null=True)
    IsActive = models.IntegerField(blank=True,null=True)
    Person = models.ForeignKey(Person,on_delete=models.CASCADE)
