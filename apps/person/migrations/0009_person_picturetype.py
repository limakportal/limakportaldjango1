# Generated by Django 3.0.8 on 2020-09-02 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0008_auto_20200827_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='PictureType',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
