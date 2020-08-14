# Generated by Django 3.1 on 2020-08-14 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('person', '0001_initial'),
        ('city', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonEducation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SchoolName', models.CharField(blank=True, max_length=100, null=True)),
                ('SchoolTypeId', models.IntegerField(blank=True, null=True)),
                ('StartDate', models.DateField(blank=True, null=True)),
                ('GraduationDate', models.DateField(blank=True, null=True)),
                ('Description', models.CharField(blank=True, max_length=200, null=True)),
                ('Degree', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('Faculty', models.CharField(blank=True, max_length=100, null=True)),
                ('ForeignLanguage', models.CharField(blank=True, max_length=200, null=True)),
                ('Section', models.BinaryField(blank=True, null=True)),
                ('City', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='city.city')),
                ('Person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='person.person')),
            ],
            options={
                'db_table': 'PersonEducation',
            },
        ),
    ]
