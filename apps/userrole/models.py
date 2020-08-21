from django.db import models
from ..account.models import Account
from ..role.models import Role


class UserRole(models.Model):
    Account = models.ForeignKey(Account,on_delete=models.CASCADE)
    Role = models.ForeignKey(Role,on_delete=models.CASCADE)

