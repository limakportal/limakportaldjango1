from django.db import models

# Create your models here.


class Personel(models.Model):
    class Meta:
        db_table = 'Personel'

    Name = models.CharField(max_length=50)
    Surname = models.CharField(max_length=50)
    Citizenship = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.Name
