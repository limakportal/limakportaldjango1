from django.db import models
from apps.status.models import Status

class City(models.Model):
    class Meta:
        db_table = 'City'

    Name = models.CharField(blank=True, max_length=50)
    PlateCode = models.IntegerField(blank=True,null=True)
    Status = models.ForeignKey(Status, on_delete = models.CASCADE,blank=True, null=True)

    def __str__(self):
        return self.Name
