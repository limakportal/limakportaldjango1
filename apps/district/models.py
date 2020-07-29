from django.db import models
from apps.status.models import Status
from apps.city.models import City

# Create your models here.


class District(models.Model):
    class Meta:
        db_table = 'District'

    Name = models.CharField(blank=True,max_length=100,null=True)
    Status = models.ForeignKey(Status,on_delete=models.CASCADE)
    City = models.ForeignKey(City,on_delete=models.CASCADE)