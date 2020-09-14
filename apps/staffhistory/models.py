from django.db import models

from ..person.models import Person
from ..organization.models import Organization
from ..title.models import Title


class StaffHistory(models.Model):
    class Meta:
        db_table = 'StaffHistory'

    Person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True, null=True)
    Organization = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=True, null=True)
    Title = models.ForeignKey(Title, on_delete=models.CASCADE, blank=True, null=True)
    EndDate = models.DateTimeField(blank=True, null=True)
    StartDate = models.DateTimeField(blank=True, null=True)
