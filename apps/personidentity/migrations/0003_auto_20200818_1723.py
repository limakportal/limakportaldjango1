# Generated by Django 3.1 on 2020-08-18 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personidentity', '0002_auto_20200817_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personidentity',
            name='BirthDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='personidentity',
            name='MilitaryDischargeData',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
