# Generated by Django 3.0.8 on 2020-08-13 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nationality', '0001_initial'),
        ('person', '0007_auto_20200813_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='Nationality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='NationalityId', to='nationality.Nationality'),
        ),
    ]