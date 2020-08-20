from django.db import models

class RightMainType(models.Model):
    class Meta:
        db_table = 'RightMainType'

    Name = models.CharField(blank=True, max_length=50,null=True)

    def __str__(self):
        return self.Name