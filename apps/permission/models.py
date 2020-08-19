from django.db import models

class Permission(models.Model):
    class Meta:
        db_table = 'Permission'

    Name = models.CharField(blank=True, max_length=50,null=True)
    Code = models.CharField(blank=True, max_length=50,null=True)
    Active = models.BooleanField(default=True)
    IsMenu = models.BooleanField(default=True)
    Icon = models.CharField(blank=True,null=True,max_length=200)
    Link = models.CharField(blank=True,null=True,max_length=200)    
    UpperPermission = models.ForeignKey('self', on_delete = models.CASCADE,blank=True, null=True)

    def children(self):
        return Permission.objects.filter(UpperPermission=self)

    @property
    def any_children(self):
        return Permission.objects.filter(UpperPermission=self).exists()

    def __str__(self):
        return self.Name
    