# Generated by Django 3.0.8 on 2020-09-14 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personemployment', '0002_auto_20200914_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personemployment',
            name='EndDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='personemployment',
            name='StartDate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
