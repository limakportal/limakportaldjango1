# Generated by Django 3.0.8 on 2020-07-23 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Personel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('Surname', models.CharField(max_length=50)),
                ('Citizenship', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'Personel',
            },
        ),
    ]
