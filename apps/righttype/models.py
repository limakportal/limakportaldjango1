from django.db import models
from apps.status.models import Status
from apps.rightmaintype.models import RightMainType

# Create your models here.


class RightType(models.Model):
    class Meta:
        db_table = 'RightType'

    Name = models.CharField(blank=True, max_length=50)
    Status = models.ForeignKey(Status, on_delete = models.CASCADE,blank=True, null=True)
    RightMainType = models.ForeignKey(RightMainType, on_delete = models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.Name