# Generated by Django 3.1 on 2020-08-17 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('city', '0002_auto_20200817_1206'),
        ('status', '0001_initial'),
        ('district', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='City',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='city.city'),
        ),
        migrations.AlterField(
            model_name='district',
            name='Status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='status.status'),
        ),
    ]
