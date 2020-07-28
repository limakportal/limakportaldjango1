from django.db import models

class Status(models.Model):
    class Meta:
        db_table = 'Status'

    Name = models.CharField(blank=True, max_length=50,null=True)