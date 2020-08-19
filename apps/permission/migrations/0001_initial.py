# Generated by Django 3.0.8 on 2020-08-19 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, max_length=50, null=True)),
                ('Code', models.CharField(blank=True, max_length=50, null=True)),
                ('Active', models.BooleanField(default=True)),
                ('IsMenu', models.BooleanField(default=True)),
                ('Icon', models.CharField(blank=True, max_length=200, null=True)),
                ('Link', models.CharField(blank=True, max_length=200, null=True)),
                ('UpperPermission', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='permission.Permission')),
            ],
            options={
                'db_table': 'Permission',
            },
        ),
    ]