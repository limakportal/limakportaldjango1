from django.db import models
from apps.account.models import Account

class Announcment(models.Model):
    class Meta:
        db_table = 'Announcment'

    Header = models.CharField(blank=True, max_length=50)
    Description = models.CharField(blank=True,max_length=500,null=True)
    StartDate = models.DateTimeField(blank=True, null=True)
    EndDate = models.DateTimeField(blank=True, null=True)
    CreatedBy = models.ForeignKey(Account, on_delete = models.CASCADE,blank=True,related_name = 'CreatedBy')
    CreationTime = models.DateTimeField(blank=True, null=True)
    ModifiedBy = models.ForeignKey(Account, on_delete = models.CASCADE,blank=True,related_name = 'ModifiedBy')
    ModificationTime = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return self.Name