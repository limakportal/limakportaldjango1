from django.db import models
from apps.status.models import Status
from apps.organizationtype.models import OrganizationType

class Organization(models.Model):
    class Meta:
        db_table = 'Organization'

    Name = models.CharField(blank=True, max_length=50,null=True)
    Status = models.ForeignKey(Status,on_delete=models.CASCADE)
    OrganizationType = models.ForeignKey(OrganizationType, on_delete=models.CASCADE)
    # Organization = models.ForeignKey(Organization, on_delete = models.CASCADE, related_name='upperorganizationid')
    
    