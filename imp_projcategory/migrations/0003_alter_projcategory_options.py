# Generated by Django 3.2.6 on 2021-10-15 01:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imp_projcategory', '0002_rename_projectcategory_projcategory_project_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projcategory',
            options={'ordering': ['project_category']},
        ),
    ]
