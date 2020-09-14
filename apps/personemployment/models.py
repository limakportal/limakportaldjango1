from django.db import models
from apps.title.models import Title
from apps.organization.models import Organization
from apps.status.models import Status
from apps.person.models import Person

class PersonEmployment(models.Model):
    class Meta:
        db_table = 'PersonEmployment'

    Person = models.ForeignKey(Person,on_delete=models.CASCADE,blank=True, null=True)
    Organization = models.ForeignKey(Organization, on_delete = models.CASCADE,blank=True, null=True)
    Title = models.ForeignKey(Title, on_delete=models.CASCADE,blank=True, null=True)
    StartDate = models.DateField(blank=True, null=True)
    EndDate = models.DateField(blank=True, null=True)
    Status = models.ForeignKey(Status,on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return self.Title