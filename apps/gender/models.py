from django.db import models

class Gender(models.Model):
    class Meta:
        db_table = 'Gender'

    Name = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.Name

 




