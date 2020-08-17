from django.db import models
from apps.status.models import Status

# Create your models here.


class RightStatus(models.Model):
    class Meta:
        db_table = 'RightStatus'

    Name = models.CharField(blank=True,max_length=100,null=True)
    Status = models.ForeignKey(Status,on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return self.Name