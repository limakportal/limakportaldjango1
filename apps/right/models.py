from django.db import models
from django.utils import timezone

from ..person.models import Person
from apps.righttype.models import RightType
from apps.rightstatus.models import RightStatus
from apps.account.models import Account


class Right(models.Model):
    class Meta:
        db_table = 'Right'

    Person = models.ForeignKey(Person, on_delete=models.CASCADE)
    EndDate = models.DateTimeField(blank=True, null=True)
    StartDate = models.DateTimeField(blank=True, null=True)
    DateOfReturn = models.DateTimeField(blank=True, null=True)
    # Address = models.CharField(max_length=50,blank=True,null=True)
    Telephone = models.CharField(max_length=50, blank=True, null=True)
    Approver1 = models.IntegerField(blank=True, null=True)
    RightType = models.ForeignKey(RightType, on_delete=models.CASCADE, blank=True, null=True)
    RightStatus = models.ForeignKey(RightStatus, on_delete=models.CASCADE, blank=True, null=True)
    RightNumber = models.DecimalField(max_digits=8, decimal_places=1, blank=True, null=True)
    DenyExplanation = models.CharField(max_length=50, blank=True, null=True)
    HrHasField = models.BooleanField(blank=True, default=False)
    KvkkIsChecked = models.BooleanField(blank=True, null=True)
    RightPicture = models.FileField(blank=True, null=True)
    CreatedDate = models.DateTimeField(blank=True, null=True)
    CreatedBy = models.ForeignKey(Account, models.SET_NULL, blank=True, null=True, related_name='RightCreatedBy')
    ModifiedDate = models.DateTimeField(blank=True, null=True)
    ModifiedBy = models.ForeignKey(Account, models.SET_NULL, blank=True, null=True, related_name='RightModifiedBy')

    def __str__(self):
        return self.Person.Name

    def save(self, *args, **kwargs):
        if not self.id:
            self.CreatedDate = timezone.now()
        else:
            self.ModifiedDate = timezone.now()

        return super(Right, self).save(*args,**kwargs)
