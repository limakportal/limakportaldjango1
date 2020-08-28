from django.db import models
from apps.announcment.models import Announcment
from apps.organization.models import Organization

class AnnouncmentOrganization(models.Model):
    class Meta:
        db_table = 'AnnouncmentOrganization'

    Announcment = models.ForeignKey(Announcment, on_delete=models.CASCADE,blank=True)
    Organization = models.ForeignKey(Organization, on_delete = models.CASCADE,blank=True)



    def __str__(self):
        return self.Name