# Generated by Django 3.2 on 2021-07-21 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imp_projcategory', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projcategory',
            old_name='projectcategory',
            new_name='project_category',
        ),
    ]
