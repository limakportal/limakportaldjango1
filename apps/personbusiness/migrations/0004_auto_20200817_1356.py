# Generated by Django 3.1 on 2020-08-17 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personbusiness', '0003_auto_20200817_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personbusiness',
            name='FirstBudget',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='personbusiness',
            name='JobStartDate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
