# Generated by Django 3.0.8 on 2020-08-19 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('role', '0001_initial'),
        ('permission', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Active', models.BooleanField(default=True)),
                ('Permission', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='permission.Permission')),
                ('Role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='role.Role')),
            ],
            options={
                'db_table': 'Authority',
            },
        ),
    ]