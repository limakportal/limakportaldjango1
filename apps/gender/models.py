from django.db import models

# Create your models here.


class Gender(models.Model):
    class Meta:
        db_table = 'Gender'

    Name = models.CharField(max_length=50,blank=True,null=True)


 




