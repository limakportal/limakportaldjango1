from django.db import models
from apps.status.models import Status

class City(models.Model):
    class Meta:
        db_table = 'City'

    Name = models.CharField(blank=True, max_length=50)
    Status = models.ForeignKey(Status, on_delete = models.CASCADE)

    def __str__(self):
        return self.Name
