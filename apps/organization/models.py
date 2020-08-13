from django.db import models
from apps.status.models import Status
from apps.organizationtype.models import OrganizationType

class Organization(models.Model):
    class Meta:
        db_table = 'Organization'

    Name = models.CharField(blank=True, max_length=50,null=True)
    Status = models.ForeignKey(Status,on_delete=models.CASCADE)
    OrganizationType = models.ForeignKey(OrganizationType, on_delete=models.CASCADE)
    UpperOrganization = models.ForeignKey('self', on_delete = models.CASCADE,null=True)

    def children(self):
        return Organization.objects.filter(UpperOrganization=self)

    @property
    def any_children(self):
        return Organization.objects.filter(UpperOrganization = self).exists()

    def __str__(self):
        return self.Name
    