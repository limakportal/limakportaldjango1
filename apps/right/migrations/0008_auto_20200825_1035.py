# Generated by Django 3.0.8 on 2020-08-25 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('right', '0007_right_ikhasfield'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='right',
            name='IKHasField',
        ),
        migrations.AddField(
            model_name='right',
            name='HrHasField',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
