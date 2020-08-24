from django.db import models

class Shift(models.Model):
    class Meta:
        db_table = 'Shift'

    Name:models.CharField(blank=True, max_length=50,null=True)
    FirstShiftStartTime : models.TimeField(auto_now=False, auto_now_add=False)
    FirstShiftEndTime : models.TimeField(auto_now=False, auto_now_add=False)
    SecondShiftStartTime : models.TimeField(auto_now=False, auto_now_add=False)
    SecondShiftEndTime : models.TimeField(auto_now=False, auto_now_add=False)
    TotalHours:models.IntegerField(blank=True, null=True)
    IsSaturDayHalfDay : models.BooleanField(blank=True, null=True)
    
    def __str__(self):
        return self.Name
