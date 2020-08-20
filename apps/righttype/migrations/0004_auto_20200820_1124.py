# Generated by Django 3.0.8 on 2020-08-20 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rightmaintype', '0001_initial'),
        ('righttype', '0003_righttype_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='righttype',
            name='Description',
        ),
        migrations.AddField(
            model_name='righttype',
            name='RightMainType',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rightmaintype.RightMainType'),
        ),
    ]
