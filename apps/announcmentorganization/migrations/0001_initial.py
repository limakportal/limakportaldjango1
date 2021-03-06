# Generated by Django 3.0.8 on 2020-08-28 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization', '0006_auto_20200828_0941'),
        ('announcment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnouncmentOrganization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Announcment', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='announcment.Announcment')),
                ('Organization', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='organization.Organization')),
            ],
            options={
                'db_table': 'AnnouncmentOrganization',
            },
        ),
    ]
