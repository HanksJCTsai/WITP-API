# Generated by Django 3.2.6 on 2021-10-15 01:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imp_bud', '0008_auto_20210916_1127'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='impbud',
            options={'ordering': ['project_year', 'project_name', 'cancelled']},
        ),
    ]
