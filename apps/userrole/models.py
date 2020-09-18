from django.db import models
from ..account.models import Account
from ..role.models import Role


class UserRole(models.Model):
    class Meta:
        db_table = 'UserRole'

    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    Role = models.ForeignKey(Role, on_delete=models.CASCADE)
    Organizations = models.CharField(blank=True, null=True, max_length=100)

    def __str__(self):
        return self.Account.email
