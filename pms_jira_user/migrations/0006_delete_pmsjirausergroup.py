# Generated by Django 3.2.12 on 2022-03-29 02:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pms_jira_user', '0005_pmsjirausergroup'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PmsJiraUserGroup',
        ),
    ]
