# Generated by Django 3.1 on 2020-08-17 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0001_initial'),
        ('righttype', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='righttype',
            name='Status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='status.status'),
        ),
    ]
