# Generated by Django 3.0.8 on 2020-09-02 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0009_person_picturetype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='PictureType',
            field=models.CharField(blank=True, default='image/png', max_length=50, null=True),
        ),
    ]
