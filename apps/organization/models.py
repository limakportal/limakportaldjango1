from django.db import models
from apps.status.models import Status
from apps.organizationtype.models import OrganizationType

from apps.title.models import Title
from ..shift.models import Shift

class Organization(models.Model):
    class Meta:
        db_table = 'Organization'

    Name = models.CharField(blank=True, max_length=200,null=True)
    Status = models.ForeignKey(Status,on_delete=models.CASCADE,blank=True, null=True)
    OrganizationType = models.ForeignKey(OrganizationType, on_delete=models.CASCADE,blank=True, null=True)
    UpperOrganization = models.ForeignKey('self', on_delete = models.CASCADE,blank=True, null=True)
    Telephone = models.CharField(blank=True,null=True,max_length=11)
    Address = models.CharField(blank=True,null=True,max_length=200)
    IsSaturdayWorkDay = models.BooleanField(default=False)
    IsSundayWorkDay = models.BooleanField(default=False)
    CanApproveRight = models.BooleanField(default=False)
    ManagerTitle = models.ForeignKey(Title, on_delete = models.CASCADE,blank=True, null=True)
    WorkStartTime = models.DateTimeField(blank=True, null=True)
    WorkEndTime = models.DateTimeField(blank=True, null=True)
    Shift = models.ForeignKey(Shift, on_delete = models.CASCADE,blank=True, null=True)
    Email = models.CharField(blank=True, null=True, max_length=50)



    def children(self):
        return Organization.objects.filter(UpperOrganization=self)

    @property
    def any_children(self):
        return Organization.objects.filter(UpperOrganization = self).exists()

    def __str__(self):
        return self.Name
    