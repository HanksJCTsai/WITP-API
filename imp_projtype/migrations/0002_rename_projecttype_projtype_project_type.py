# Generated by Django 3.2 on 2021-07-21 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imp_projtype', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projtype',
            old_name='Projecttype',
            new_name='Project_type',
        ),
    ]
