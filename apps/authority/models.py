from django.db import models
from apps.organization.models import Organization
from apps.role.models import Role
from apps.permission.models import Permission

class Authority(models.Model):
    class Meta:
        db_table = 'Authority'

    Role = models.ForeignKey(Role, on_delete = models.CASCADE,blank=True, null=True)
    Permission = models.ForeignKey(Permission,on_delete=models.CASCADE,blank=True, null=True)
    Active = models.BooleanField(default=True)


    def __str__(self):
        return self.Role.Name