from django.db import models

class NavigationBar(models.Model):
    class Meta:
        db_table = 'NavigationBar'

    label = models.CharField(max_length=100 , blank=True, null=True)
    icon = models.CharField(max_length=100 , blank=True, null=True)
    to = models.CharField(max_length=100 , blank=True, null=True)
    root = models.ForeignKey('self', on_delete = models.CASCADE,blank=True, null=True,related_name='items')

    def __str__(self):
        return self.label

    def children(self):
        return NavigationBar.objects.filter(root=self)

    @property
    def any_children(self):
        return NavigationBar.objects.filter(root = self).exists()

