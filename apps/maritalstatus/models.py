from django.db import models

class MaritalStatus(models.Model):
    class Meta:
        db_table = 'MaritalStatus'

    Name = models.CharField(max_length=50,blank=True,null=True)


 




