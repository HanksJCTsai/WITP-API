# Generated by Django 3.1.7 on 2022-01-20 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pms_project_version_control', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pmsprojectversioncontrol',
            old_name='project_id',
            new_name='project',
        ),
    ]
