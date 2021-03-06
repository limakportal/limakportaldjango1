# Generated by Django 3.1 on 2020-08-14 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rightstatus', '0001_initial'),
        ('right', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RightHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ChangedBy', models.IntegerField(blank=True, null=True)),
                ('ChangedDate', models.DateField(auto_now_add=True, max_length=50, null=True)),
                ('Right', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='right.right')),
                ('RightStatus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rightstatus.rightstatus')),
            ],
            options={
                'db_table': 'RightHistory',
            },
        ),
    ]
