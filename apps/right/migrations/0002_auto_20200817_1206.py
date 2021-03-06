# Generated by Django 3.1 on 2020-08-17 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rightstatus', '0001_initial'),
        ('righttype', '0001_initial'),
        ('right', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='right',
            name='DenyExplanation',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='right',
            name='RightStatus',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rightstatus.rightstatus'),
        ),
        migrations.AlterField(
            model_name='right',
            name='RightType',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='righttype.righttype'),
        ),
    ]
