# Generated by Django 3.2.12 on 2022-05-06 03:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pms_project_user', '0007_alter_pmsprojectuser_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pmsprojectuserlog',
            name='sign',
        ),
    ]
