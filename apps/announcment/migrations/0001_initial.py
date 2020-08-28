# Generated by Django 3.0.8 on 2020-08-28 08:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Header', models.CharField(blank=True, max_length=50)),
                ('Description', models.CharField(blank=True, max_length=500, null=True)),
                ('StartDate', models.DateTimeField(blank=True, null=True)),
                ('EndDate', models.DateTimeField(blank=True, null=True)),
                ('CreationTime', models.DateTimeField(blank=True, null=True)),
                ('ModificationTime', models.DateTimeField(blank=True, null=True)),
                ('CreatedBy', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='CreatedBy', to=settings.AUTH_USER_MODEL)),
                ('ModifiedBy', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='ModifiedBy', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Announcment',
            },
        ),
    ]