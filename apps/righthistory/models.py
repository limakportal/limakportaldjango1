from django.db import models
from apps.right.models import Right
from apps.rightstatus.models import RightStatus

class RightHistory(models.Model):
    class Meta:
        db_table = 'RightHistory'

    Right = models.ForeignKey(Right,on_delete=models.CASCADE)
    ChangedBy = models.IntegerField(blank=True,null=True)
    ChangedDate = models.DateField(auto_now_add=True,max_length=50,blank=True,null=True)
    RightStatus = models.ForeignKey(RightStatus,on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return self.Right
