# Generated by Django 3.0.8 on 2020-09-14 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization', '0006_auto_20200828_0941'),
        ('status', '0001_initial'),
        ('person', '0010_auto_20200903_0021'),
        ('title', '0002_auto_20200817_1206'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonEmployment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StartDate', models.DateField(blank=True, null=True)),
                ('EndDate', models.DateField(blank=True, null=True)),
                ('Organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.Organization')),
                ('Person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='person.Person')),
                ('Status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='status.Status')),
                ('Title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='title.Title')),
            ],
            options={
                'db_table': 'PersonEmployment',
            },
        ),
    ]
