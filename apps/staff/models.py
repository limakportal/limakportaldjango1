from django.db import models
from apps.title.models import Title
from apps.role.models import Role
from apps.organization.models import Organization
from apps.status.models import Status
from apps.person.models import Person

class Staff(models.Model):
    class Meta:
        db_table = 'Staff'

    Title = models.ForeignKey(Title, on_delete=models.CASCADE)
    Role = models.ForeignKey(Role, on_delete=models.CASCADE)
    Organization = models.ForeignKey(Organization, on_delete = models.CASCADE,blank=True, null=True)
    Status = models.ForeignKey(Status,on_delete=models.CASCADE,blank=True, null=True)
    Person = models.ForeignKey(Person,on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return self.Person.Name