from django.db import models
from apps.status.models import Status

# Create your models here.


class Title(models.Model):
    class Meta:
        db_table = 'Title'

    Name = models.CharField(blank=True, max_length=50)
    Status = models.ForeignKey(Status, on_delete = models.CASCADE,blank=True, null=True)

    def __str__(self):
        return self.Name