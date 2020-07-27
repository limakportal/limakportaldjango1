# Generated by Django 3.0.8 on 2020-07-27 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Email', models.CharField(max_length=50)),
                ('Password', models.CharField(max_length=50)),
                ('IsApproved', models.IntegerField(blank=True, null=True)),
                ('IsActive', models.IntegerField(blank=True, null=True)),
                ('Person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='person.Person')),
            ],
            options={
                'db_table': 'User',
            },
        ),
    ]
