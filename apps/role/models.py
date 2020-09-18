from django.db import models

class Role(models.Model):
    class Meta:
        db_table = 'Role'

    Name = models.CharField(blank=True, max_length=50)
    IsHierarchical = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.Name