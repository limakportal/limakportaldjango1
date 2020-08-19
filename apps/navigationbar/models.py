from django.db import models

class NavigationBar(models.Model):
    class Meta:
        db_table = 'NavigationBar'

    Lable = models.CharField(max_length=100 , blank=True, null=True)
    Icon = models.CharField(max_length=100 , blank=True, null=True)
    To = models.CharField(max_length=100 , blank=True, null=True)
    Root = models.ForeignKey('self', on_delete = models.CASCADE,blank=True, null=True)

    def __str__(self):
        return self.Lable
