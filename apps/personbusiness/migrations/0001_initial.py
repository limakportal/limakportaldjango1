# Generated by Django 3.1 on 2020-08-17 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('person', '0002_auto_20200817_1206'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonBusiness',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ContractType', models.IntegerField(blank=True, null=True)),
                ('JobStartDate', models.DateField(blank=True, null=True)),
                ('FirstBudget', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('JobCode', models.CharField(blank=True, max_length=100, null=True)),
                ('RegisterNo', models.CharField(blank=True, max_length=100, null=True)),
                ('SGKRegisterNo', models.CharField(blank=True, max_length=100, null=True)),
                ('SGKEnterDate', models.DateField(auto_now_add=True, max_length=50, null=True)),
                ('Person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='person.person')),
            ],
            options={
                'db_table': 'PersonBusiness',
            },
        ),
    ]
