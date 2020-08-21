# Generated by Django 3.0.8 on 2020-08-20 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('person', '0005_auto_20200818_1613'),
    ]

    operations = [
        migrations.CreateModel(
            name='RightLeave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Earning', models.IntegerField(blank=True, null=True)),
                ('Year', models.DateField(blank=True, null=True)),
                ('Optime', models.DateTimeField(blank=True, null=True)),
                ('Person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='person.Person')),
            ],
            options={
                'db_table': 'RightLeave',
            },
        ),
    ]