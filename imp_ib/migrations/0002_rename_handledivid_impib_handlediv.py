# Generated by Django 3.2 on 2021-07-21 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imp_ib', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='impib',
            old_name='handledivid',
            new_name='handlediv',
        ),
    ]
