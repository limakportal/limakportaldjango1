from django.db import models
from apps.status.models import Status

class VocationDays(models.Model):
    class Meta:
        db_table = 'VocationDays'

    Name = models.CharField(blank=True, max_length=50)
    DateDay = models.DateTimeField(blank=True,null=True)
    DayType = models.BooleanField(blank=True,null=True)

    def __str__(self):
        return self.Name
