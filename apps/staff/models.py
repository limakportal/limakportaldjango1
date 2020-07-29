from django.db import models
from apps.title.models import Title
from apps.organization.models import Organization
from apps.status.models import Status
from apps.person.models import Person

# Create your models here.


class Staff(models.Model):
    class Meta:
        db_table = 'Staff'

    Title = models.ForeignKey(Title, on_delete=models.CASCADE)
    Organization = models.ForeignKey(Organization, on_delete = models.CASCADE)
    Status = models.ForeignKey(Status,on_delete=models.CASCADE)
    Person = models.ForeignKey(Person,on_delete=models.CASCADE)