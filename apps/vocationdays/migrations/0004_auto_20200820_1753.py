# Generated by Django 3.0.8 on 2020-08-20 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vocationdays', '0003_auto_20200820_1414'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vocationdays',
            old_name='Date',
            new_name='DateDay',
        ),
    ]