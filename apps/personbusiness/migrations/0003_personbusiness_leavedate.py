# Generated by Django 3.0.8 on 2020-08-25 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personbusiness', '0002_auto_20200818_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='personbusiness',
            name='LeaveDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
