# Generated by Django 3.0.8 on 2020-07-29 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('status', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, max_length=50)),
                ('Status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='status.Status')),
            ],
            options={
                'db_table': 'OrganizationType',
            },
        ),
    ]
