from django.db import models

class Nationality(models.Model):
    class Meta:
        db_table = 'Nationality'

    Name = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.Name


 




